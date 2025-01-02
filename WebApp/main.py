from flask import Flask, render_template, redirect, url_for, request, flash, session, Response, jsonify, g
import mysql.connector
import pandas as pd
import numpy as np
import cv2
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from sklearn.metrics.pairwise import cosine_similarity
from io import BytesIO
from PIL import Image
from datetime import datetime
import os
from multiprocessing import Queue

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"


dtb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='super123',
    database='gp2425',
    port='3306'
)

# dtb = mysql.connector.connect(
#     host="db",  # Service name in docker-compose.yml
#     user="root",
#     password="super123",
#     database="GP2425",
#     port='3306'
# )

def delete(row_id):
    cursor = dtb.cursor(dictionary=True)
    
    cursor.execute("DELETE FROM course WHERE id = %s", (row_id,))
    dtb.commit()
    
    cursor.execute("SET @row_number = 0;")
    cursor.execute("""
        UPDATE course SET id = (@row_number:=@row_number + 1)
        ORDER BY id;
    """)
    
    dtb.commit()
    

def fetch_reference_embedding(student_id):
    cursor = dtb.cursor()
    try:
        # Fetch the image data from the database
        cursor.execute("SELECT image_data FROM image_storage WHERE student_id = %s", (student_id,))
        results = cursor.fetchall()
        if results:
            embeddings = []
            for result in results:
                blob_data = result[0]
                img = Image.open(BytesIO(blob_data)).convert("RGB")
                img = np.array(img)

                # Preprocess and extract FaceNet embedding
                img_tensor = preprocess_image(img)
                with torch.no_grad():
                    embedding = facenet(img_tensor.to(device)).cpu().numpy()
                    embeddings.append(embedding)
            aggregated_embedding = np.mean(embeddings, axis=0)
            return aggregated_embedding
        else:
            print("No image found in the database")
            return None
    finally:
        cursor.close()   

def fetch_reference_student(student_id):
    cursor = dtb.cursor()
    try:
        cursor.execute("SELECT student_name FROM student_infor WHERE student_id = %s", (student_id,))
        student_info = cursor.fetchone()
        return student_info
    finally:
        cursor.fetchall()
        cursor.close()

def preprocess_image(img, target_size=(160, 160)):
    img = cv2.resize(img, target_size)  # Resize the image
    img = img.astype('float32') / 255.0  # Normalize pixel values
    img = np.transpose(img, (2, 0, 1))  # Convert HWC to CHW for PyTorch
    img = torch.tensor(img).unsqueeze(0).float()  # Add batch dimension
    return img

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(f"Running on device: {device}")

# Initialize FaceNet model and MTCNN
facenet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20, thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True, device=device)
matched_data_queue = Queue()

def generate_frames(student_id):
    # Fetch the reference embedding
    reference_embedding = fetch_reference_embedding(student_id)
    if reference_embedding is None:
        raise ValueError("No reference image found for the student.")

    camera = cv2.VideoCapture(0)
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                frame = cv2.flip(frame, 1)

            # Detect faces in the frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes, _ = mtcnn.detect(rgb_frame)
            if boxes is not None:
                for (x1, y1, x2, y2) in boxes:
                    # Ensure coordinates are integers and within frame bounds
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    if x1 < 0 or y1 < 0 or x2 > frame.shape[1] or y2 > frame.shape[0]:
                        continue
                    
                    # Extract the face ROI
                    face = rgb_frame[y1:y2, x1:x2]
                    if face.size == 0:  # Check if face ROI is valid
                        continue

                    # Preprocess the face and extract embeddings
                    face_tensor = preprocess_image(face)
                    with torch.no_grad():
                        live_embedding = facenet(face_tensor.to(device)).cpu().numpy()

                    # Compute cosine similarity
                    similarity = cosine_similarity(live_embedding, reference_embedding)[0][0]
                    print(f"Similarity: {similarity}")

                    # Check similarity threshold
                    if similarity > 0.83 and matched_data_queue.empty(): 
                        student_info = fetch_reference_student(student_id)
                        if student_info:
                            student_name = student_info[0]
                            matched_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            matched_data = {
                                "student_id": student_id,
                                "student_name": student_name,
                                "matched_time": matched_time,
                            }
                            matched_data_queue.put(matched_data)
                            break
                

            # Encode the frame for streaming
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    finally:
        camera.release()


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['choice']
        
        cursor = dtb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_auth WHERE account = %s AND password = %s AND role = %s", (email, password, role))
        user = cursor.fetchone()  
        
        if not user:
            flash('Invalid credentials, please try again.')
            return redirect(url_for('homepage'))   
        session['nameoflecturer'] = user['nameoflecturer']
        session['student_id'] = user['student_id']
        if user:
            if role == 'Lecturer':
                return redirect(url_for('lecturers'))
            elif role == 'Student':
                return redirect(url_for('students'))
        
    
    return render_template('homepage.html')
    
@app.route('/Lecturers')
def lecturers():
    return redirect(url_for('information'))

@app.route('/Students')
def students():
    return redirect(url_for('std_classroom'))

@app.route('/information', methods=['GET', 'POST'])
def information():
    name = session.get('nameoflecturer')
        
    if request.method == 'POST':
        row_id = request.form['row_id']
        action = request.form['action']
        
        if action == 'delete':    
            delete(row_id)
            return redirect(url_for('information'))
        if action =='view':
            session['classroom_id'] = row_id
            return redirect(url_for('addstudent'))
        
    cursor = dtb.cursor()
    cursor.execute("SELECT * FROM course WHERE nameoflecturer = %s", (name,))
    
    classroom_data = cursor.fetchall()
    
    return render_template("/Lecturer/Information.html", classroom_data=classroom_data)

@app.route('/classroom', methods=["GET", "POST"])
def classroom():
    if request.method == 'POST':
        class_name = request.form['className']
        lecturer_name = request.form['lecturerName']
        major = request.form['major']
        start_date = request.form['startDate']
        end_date = request.form['endDate']   
        
        cursor = dtb.cursor(dictionary=True)

        cursor.execute("SELECT * FROM course WHERE nameofclass = %s AND major = %s", (class_name, major))
        exist_class = cursor.fetchone()
        
        if exist_class:
            flash('This class already exists !')
            return redirect('classroom')
        else:
            cursor.execute('''
                INSERT INTO course (nameofclass, nameoflecturer, major, begindate, enddate)
                VALUES (%s, %s, %s, %s, %s)
            ''', (class_name, lecturer_name, major, start_date, end_date))
            
            dtb.commit()
        
        cursor.execute("SET @row_number = 0;")
        cursor.execute("""
            UPDATE course SET id = (@row_number:=@row_number + 1)
            ORDER BY id;
        """)
    
        dtb.commit()
        return redirect(url_for('information'))       
        
    return render_template("/Lecturer/Classroom.html")

@app.route('/addstudent', methods=["GET", "POST"])
def addstudent(): 
    classroom_id = session.get('classroom_id')
    
    if request.method == "POST":
        file = request.files.get('file')

        if file:
            try:
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.filename.endswith('.xlsx'):
                    df = pd.read_excel(file)
                else:
                    flash("Unsupported file format.", "danger")
                    return redirect(url_for('addstudent'))
                 
                cursor = dtb.cursor()
                
                added_students = []
                existing_students = []

                # Iterate through the DataFrame
                for _, row in df.iterrows():
                    student_id = row.get('Student id')  # Adjust column name if needed
                    if not student_id:
                        continue  # Skip rows without a valid student_id

                    # Check if the student exists in the database
                    cursor.execute(
                        "SELECT * FROM student_infor WHERE student_id = %s", (student_id,)
                    )
                    existing_student = cursor.fetchone()

                    if existing_student:
                        # Check if the student is already in the course
                        cursor.execute(
                            "SELECT * FROM student_in_course WHERE student_id = %s AND course_id = %s",
                            (student_id, classroom_id)
                        )
                        student_in_course = cursor.fetchone()

                        if student_in_course:
                            existing_students.append(student_id)
                        else:
                            # Insert student into the course
                            cursor.execute(
                                "INSERT INTO student_in_course (student_id, course_id) VALUES (%s, %s)",
                                (student_id, classroom_id)
                            )
                            added_students.append(student_id)

                # Commit changes to the database
                dtb.commit()

                # Flash messages
                if added_students:
                    flash(f"Added {len(added_students)} students to the course.", "success")
                if existing_students:
                    flash(f"The following students were already in the course: {', '.join(existing_students)}.", "warning")
            
            except Exception as e:
                dtb.rollback()
                flash(f"An error occurred: {str(e)}", "danger")
            finally:
                cursor.close()

    # Fetch students associated with the course for display
    try:
        cursor = dtb.cursor()
        cursor.execute("""
            SELECT s.student_id, si.student_name, si.major, si.student_id AS face_id
            FROM student_in_course s
            JOIN student_infor si ON s.student_id = si.student_id
            WHERE s.course_id = %s
        """, (classroom_id,))
        students = cursor.fetchall()
        cursor.close()
    except Exception as e:
        flash(f"Failed to fetch students: {str(e)}", "danger")
            
    return render_template("/Lecturer/AddStudent.html", students=students)

@app.route('/attandence', methods=['GET', 'POST'])
def attendance():
    name = session.get('nameoflecturer')
    if request.method == "POST":
        row_id = request.form['row_id']
        action = request.form['action']
        session['classroom_id'] = row_id
        
        if action =='view':
            return redirect(url_for('attendance_information'))
        
    cursor = dtb.cursor()
    cursor.execute("SELECT * FROM course WHERE nameoflecturer = %s", (name,))
    classroom_data = cursor.fetchall()
    return render_template("/Lecturer/Attendance.html", classroom_data=classroom_data)

@app.route('/attendance information', methods=['GET', 'POST'])
def attendance_information():
    classroom_id = session.get('classroom_id')
    
    if request.method == 'POST':
        if 'action' in request.form:
            action = request.form['action']
            row_id = request.form['row_id']
            
            if action == 'view':
                session['checked_id'] = row_id
                return redirect(url_for('checking'))
            if action == 'delete':
                cursor = dtb.cursor(dictionary=True)
                cursor.execute("DELETE FROM attendance_checked WHERE id = %s", (row_id,))
                dtb.commit()
    
                cursor.execute("SET @row_number = 0;")
                cursor.execute("""
                    UPDATE attendance_checked SET id = (@row_number:=@row_number + 1)
                    ORDER BY id;
                """)
                dtb.commit()
                
                return redirect(url_for('attendance_information'))
        
        start_time = request.form['start_time']
        place = request.form['place']
        
        try:            
            cursor = dtb.cursor()
            cursor.execute("INSERT INTO attendance_checked (start_time, place, course_id) VALUES (%s, %s, %s)",
                        (start_time, place, classroom_id,))
            dtb.commit()
            flash("Attendance record successfully created!")
            
            cursor.execute("SET @row_number = 0;")
            cursor.execute("""
                UPDATE attendance_checked SET id = (@row_number:=@row_number + 1)
                ORDER BY id;
            """)
            dtb.commit()
        except Exception as e:
            flash(f"Error: {e}")
        return redirect(url_for('attendance_information'))
    
    now = datetime.now()
    currentDateTime = now.strftime("%Y-%m-%dT%H:%M")
    
    cursor = dtb.cursor()
    cursor.execute("SELECT id, start_time, place FROM attendance_checked WHERE course_id = %s", (classroom_id,))
    checked = cursor.fetchall()  
    return render_template("/Lecturer/attendance_information.html", currentDateTime=currentDateTime, checked=checked)

@app.route('/checking', methods=['GET', 'POST'])
def checking():
    checked_id = session.get('checked_id')
    
    cursor = dtb.cursor()
    cursor.execute("""
                   SELECT si.student_name, sa.student_id, sa.time_checking
                   FROM student_attendance sa
                   JOIN student_infor_details sid ON sa.student_id = sid.student_id
                   JOIN student_infor si ON sid.student_id = si.student_id
                   WHERE sa.attendance_id = %s
                    """, (checked_id,))
    checked_list = cursor.fetchall()
    return render_template('/Lecturer/attendance_checking.html', checked_list=checked_list)

@app.route('/std_information', methods=['GET', 'POST'])
def std_information():
    student_id = session.get('student_id')
    
    if not student_id:
        flash("You are not logged in!", "danger")
        return redirect(url_for('login'))

    try:
        cursor = dtb.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                si.student_id, si.student_name, sid.birthday, sid.birthplace,
                sid.household_registration, sid.citizen_identification,
                sid.telephone, sid.email, si.major, sid.training_system,
                sid.class, sid.course
            FROM student_infor si
            JOIN student_infor_details sid ON si.student_id = sid.student_id
            WHERE si.student_id = %s
        """, (student_id,))
        
        details = cursor.fetchone()
        
        if not details:
            flash("Student details not found!", "warning")
            return redirect(url_for('homepage'))
        
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        details = None
    finally:
        cursor.close()
    return render_template('/Student/information.html', details=details)

@app.route('/std_classroom', methods=['GET', 'POST'])
def std_classroom():
    std_id = session.get('student_id')
    
    if request.method == "POST":
        row_id = request.form['row_id']
        action = request.form['action']
        if action == "view":
            session['row_id'] = row_id
            return redirect(url_for('std_list'))
    cursor = dtb.cursor()
    query = """
    SELECT c.id, c.nameofclass, c.major, c.begindate, c.enddate, c.nameoflecturer
    FROM student_in_course sc
    JOIN course c ON sc.course_id = c.id
    JOIN student_infor si ON sc.student_id = si.student_id
    WHERE si.student_id = %s
    """
    cursor.execute(query, (std_id,))
    
    student_data = cursor.fetchall()    
    
    return render_template('/Student/classroom.html', student_data=student_data)

@app.route('/std_list', methods=['GET', 'POST'])
def std_list():
    row_id = session.get('row_id')
    
    cursor = dtb.cursor()
    cursor.execute("""
                    SELECT s.student_id, s.student_name, s.major
                    FROM student_infor s
                    JOIN student_in_course sc ON s.student_id = sc.student_id
                    WHERE sc.course_id = %s
                """, (row_id,))
    students = cursor.fetchall()

    return render_template('/Student/student_list.html', students=students)

@app.route('/attendance', methods=['GET', 'POST'])
def std_attendance():
    std_id = session.get('student_id')
    
    if request.method == "POST":
        row_id = request.form['row_id']
        action = request.form['action']
        session['classroom_id'] = row_id
    
        if action == "view": 
            return redirect(url_for('attendance_list'))
        
    cursor = dtb.cursor()
    query = """
    SELECT c.id, c.nameofclass, c.major, c.begindate, c.enddate, c.nameoflecturer
    FROM student_in_course sc
    JOIN course c ON sc.course_id = c.id
    JOIN student_infor si ON sc.student_id = si.student_id
    WHERE si.student_id = %s
    """
    cursor.execute(query, (std_id,))
    
    classrooms = cursor.fetchall()
    return render_template('/Student/attendance.html', classrooms=classrooms)

@app.route('/attendance_list', methods=['GET', 'POST'])
def attendance_list():
    classroom_id = session.get('classroom_id')
    student_id = session.get('student_id')
    
    
    if request.method == "POST":
        row_id = request.form['row_id']
        print(f'row_id: {row_id}')
        action = request.form['action']
        
        cursor = dtb.cursor(dictionary=True)
        cursor.execute("SELECT end_time FROM attendance_checked WHERE id = %s", (row_id,))
        attendance = cursor.fetchone()
        
        if action == 'view':
            session['row_id'] = row_id
            return redirect(url_for('std_attendance_view'))
        
            
        if action == 'checking':
            if datetime.now() <= attendance['end_time']:
                cursor = dtb.cursor()
                cursor.execute("SELECT student_id FROM student_attendance WHERE attendance_id = %s", (row_id,))
                check = cursor.fetchone()
            
                if check is None or student_id not in check:
                    session['checked_id'] = row_id
                    return redirect(url_for('face_scan'))
                elif student_id in check:
                    cursor = dtb.cursor()
                    cursor.execute("SELECT start_time FROM attendance_checked WHERE id = %s", (row_id,))
                    date = cursor.fetchone()
                    flash(f"You have checked for {date[0]} !!!")
                    return redirect(url_for('attendance_list'))
            else:
                flash("The time to checking is up! You can't check acttendance.")
                return redirect(url_for('attendance_list'))
        
    current_time = datetime.now()        
    cursor = dtb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM attendance_checked WHERE course_id = %s", (classroom_id,))
    attendances = cursor.fetchall()
    return render_template('/Student/attendance_list.html', attendances=attendances, current_time=current_time)

@app.route('/view_attendance', methods=['GET', 'POST'])
def std_attendance_view():
    row_id = session.get('row_id')
    
    cursor = dtb.cursor()
    cursor.execute("""
                   SELECT si.student_name, sa.student_id, sa.time_checking
                   FROM student_attendance sa
                   JOIN student_infor_details sid ON sa.student_id = sid.student_id
                   JOIN student_infor si ON sid.student_id = si.student_id
                   WHERE sa.attendance_id = %s 
                    """, (row_id,))
    checked_list = cursor.fetchall()
    
    
    return render_template('/Student/attendance_view.html', checked_list=checked_list)


@app.route('/face_scan', methods=['GET', 'POST'])
def face_scan():
    if request.method == 'GET':
        return render_template('/Student/facescan.html')
    
    student_id = session.get('student_id')
    print(f"student id: {student_id}")
    
    if not student_id:
        return jsonify({"status": "error", "message": "Please log in to access this feature."}), 403
    
    if not matched_data_queue.empty():
        matched_data = matched_data_queue.get()                      
        
        return jsonify({
            "status": "success",
            "student_name": matched_data["student_name"],
            "student_id": matched_data["student_id"],
            "matched_time": matched_data["matched_time"]
        })
        
    return jsonify({"status": "pending"})

@app.route('/video_feed')
def video_feed():
    student_id = session.get('student_id')
    return Response(generate_frames(student_id), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    if request.method == "POST":
        student_id = request.form['studentid']
        matched_time = request.form['time']
        checked_id = session.get('checked_id')
        
        session['row_id'] = checked_id
        
        cursor = dtb.cursor()
        cursor.execute("""
                       INSERT INTO student_attendance(student_id, time_checking, attendance_id)
                       VALUES (%s, %s, %s)""", (student_id, matched_time, checked_id,))
        dtb.commit()
    
        return redirect(url_for('std_attendance_view'))
    
    return redirect(url_for('std_attendance_view'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
