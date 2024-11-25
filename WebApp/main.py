from flask import Flask, render_template, redirect, url_for, request, flash, session, Response
import mysql.connector
import pandas as pd
import numpy as np
import cv2
import tensorflow as tf
from io import BytesIO
from PIL import Image
from datetime import datetime
from waitress import serve
import os
import json

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"


dtb = mysql.connector.connect(
    host="127.0.0.1",  
    user="root",       
    password="super123",      
    database="gp2425" 
)

def delete(row_id):
    cursor = dtb.cursor(dictionary=True)
    
    cursor.execute("DELETE FROM classroom WHERE id = %s", (row_id,))
    dtb.commit()
    
    cursor.execute("SET @row_number = 0;")
    cursor.execute("""
        UPDATE classroom SET id = (@row_number:=@row_number + 1)
        ORDER BY id;
    """)
    
    dtb.commit()
    

def fetch_reference_image(student_id):
    cursor = dtb.cursor()
    try:
        cursor.execute("SELECT image_data FROM image_storage WHERE student_id = %s", (student_id,))
        result = cursor.fetchone()  # Fetch the result explicitly
        if result:
            blob_data = result[0]
            img = Image.open(BytesIO(blob_data))  # Convert BLOB to PIL Image
            img = img.convert("L")  # Convert to grayscale
            img = np.array(img)  # Convert to NumPy array
            return preprocess_image(img)
        else:
            print("No image found in database")
            return None
    finally:
        cursor.fetchall()  # Ensure any remaining results are fetched (clears buffer)
        cursor.close()   

def fetch_reference_student(student_id):
    cursor = dtb.cursor()
    try:
        cursor.execute("SELECT student_name FROM student_information WHERE student_id = %s", (student_id,))
        student_info = cursor.fetchone()  # Explicitly fetch results
        return student_info
    finally:
        cursor.fetchall()  # Clear remaining results
        cursor.close()

def preprocess_image(img, target_size=(105, 105)):
    if len(img.shape) == 2:  # If grayscale
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)  # Convert to 3 channels (RGB)
    img = cv2.resize(img, target_size)  # Resize to match model's input size
    img = img.astype('float32') / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

class L1Dist(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__()

    def call(self, inputs):
        input_embedding, validation_embedding = inputs
        return tf.math.abs(input_embedding - validation_embedding)

tf.keras.utils.get_custom_objects()["L1Dist"] = L1Dist

def generate_frames(student_id):
    # Load the Siamese model
    siamese = tf.keras.models.load_model("Model/siamesemodel.h5")
    
    # Fetch the reference image for the given student ID
    reference_image = fetch_reference_image(student_id)
    if reference_image is None:
        raise ValueError("No reference image found for the student.")
        
    camera = cv2.VideoCapture(0)
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                frame = cv2.flip(frame, 1)

            face = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Ensure 3-channel input for the model  
            processed_face = preprocess_image(face)  
            student_fetch = fetch_reference_student(student_id)
            
            if processed_face is None:
                label = "Error: Invalid Input"
                color = (0, 0, 255)  # Red for error
            else:
                similarity = siamese.predict([reference_image, processed_face])
                label = "Matched" if similarity > 0.5 else "Not Matched"
                color = (0, 255, 0) if label == "Matched" else (0, 0, 255)
                print(f'prediction: {similarity}\nlabel: {label}')

                if label == "Matched":
                    print(f"{student_fetch}\n{student_id}")
                    break
            
            cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        camera.release()

    

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['choice']
        
        cursor = dtb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_auth WHERE email = %s AND password = %s AND role = %s", (email, password, role))
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
    cursor.execute("SELECT * FROM classroom WHERE nameoflecturer = %s", (name,))
    
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

        cursor.execute("SELECT * FROM classroom WHERE nameofclass = %s AND major = %s", (class_name, major))
        exist_class = cursor.fetchone()
        
        if exist_class:
            flash('This class already exists !')
            return redirect('classroom')
        else:
            cursor.execute('''
                INSERT INTO classroom (nameofclass, nameoflecturer, major, begindate, enddate)
                VALUES (%s, %s, %s, %s, %s)
            ''', (class_name, lecturer_name, major, start_date, end_date))
            
            dtb.commit()
        
        cursor.execute("SET @row_number = 0;")
        cursor.execute("""
            UPDATE classroom SET id = (@row_number:=@row_number + 1)
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
                new_students = []
                updated_classrooms = []
                for _, row in df.iterrows():
                    cursor.execute(
                        "SELECT * FROM student_information WHERE student_id = %s", (row['Student id'],)
                    )
                    existing_student = cursor.fetchone()
                    
                    if not existing_student:
                        cursor.execute(
                            "INSERT INTO student_information (student_name, student_id, major) VALUES (%s, %s, %s)",
                            (row['Student name'], row['Student id'], row['Major'])
                        )
                        new_students.append((row['Student name'], row['Student id']))
                        dtb.commit()
                        
                    cursor.execute(
                        "SELECT * FROM student_classroom WHERE student_id = %s AND classroom_id = %s",
                        (row['Student id'], classroom_id)
                    )
                    existing_classroom = cursor.fetchone()    
                        
                    if not existing_classroom:
                        cursor.execute(
                            "INSERT INTO student_classroom (student_id, classroom_id) "
                            "VALUES (%s, %s)",
                            (row['Student id'], classroom_id)
                        )
                        updated_classrooms.append((row['Student name'], row['Student id']))
                dtb.commit()
                
                if new_students:
                    for student_name, student_id in new_students:
                        flash(f'Student {student_name} (ID: {student_id}) has been inserted into the database.')
                if updated_classrooms:
                    for student_name, student_id in updated_classrooms:
                        flash(f'Student {student_name} (ID: {student_id}) has been added to classroom {classroom_id}.')
                if not new_students and not updated_classrooms:
                    flash('No new students were added or updated.')

                return redirect(url_for('addstudent'))
            

            except Exception as e:
                flash(f"An error occurred: {str(e)}", "danger")
                return redirect(url_for('addstudent'))
        else:
            flash("No file selected.", "warning")
            return redirect(url_for('addstudent'))
        
    cursor = dtb.cursor()   
    cursor.execute("""
        SELECT s.student_id, s.student_name, s.major, s.face_id
        FROM student_information s
        JOIN student_classroom sc ON s.student_id = sc.student_id
        WHERE sc.classroom_id = %s
    """, (classroom_id,))
    students = cursor.fetchall()
    
    cursor.execute("SET @row_number = 0;")
    cursor.execute("""
        UPDATE student_information SET id = (@row_number:=@row_number + 1)
        ORDER BY id;
    """)
    
    dtb.commit()
           
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
    cursor.execute("SELECT * FROM classroom WHERE nameoflecturer = %s", (name,))
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
        
        date = request.form['date']
        time = request.form['time']
        place = request.form['place']
        
        try:            
            cursor = dtb.cursor()
            cursor.execute("INSERT INTO attendance_checked (date, time, place, classroom_id) VALUES (%s, %s, %s, %s)",
                        (date, time, place, classroom_id,))
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
    currentDate = now.strftime("%Y-%m-%d")
    currentTime = now.strftime("%H:%M")
    
    cursor = dtb.cursor()
    cursor.execute("SELECT id, date, time, place FROM attendance_checked WHERE classroom_id = %s", (classroom_id,))
    checked = cursor.fetchall()    
    return render_template("/Lecturer/attendance_information.html", currentDate=currentDate, currentTime=currentTime, checked=checked)

@app.route('/checking', methods=['GET', 'POST'])
def checking():
    return render_template('/Lecturer/attendance_checking.html')

@app.route('/std_information', methods=['GET', 'POST'])
def std_information():
    return render_template('/Student/information.html')

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
    FROM student_classroom sc
    JOIN classroom c ON sc.classroom_id = c.id
    JOIN student_information si ON sc.student_id = si.student_id
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
                    SELECT s.student_id, s.student_name, s.major, s.face_id
                    FROM student_information s
                    JOIN student_classroom sc ON s.student_id = sc.student_id
                    WHERE sc.classroom_id = %s
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
            return redirect(url_for('std_attendance_view'))
        if action == 'checking':
            return redirect(url_for('std_attendance_checking'))
    cursor = dtb.cursor()
    query = """
    SELECT c.id, c.nameofclass, c.major, c.begindate, c.enddate, c.nameoflecturer
    FROM student_classroom sc
    JOIN classroom c ON sc.classroom_id = c.id
    JOIN student_information si ON sc.student_id = si.student_id
    WHERE si.student_id = %s
    """
    cursor.execute(query, (std_id,))
    
    classrooms = cursor.fetchall()
    return render_template('/Student/attendance.html', classrooms=classrooms)

@app.route('/view_attendance', methods=['GET', 'POST'])
def std_attendance_view():
    return render_template('/Student/attendance_view.html')

@app.route('/checking_attendance', methods=['GET', 'POST'])
def std_attendance_checking():
    classroom_id = session.get('classroom_id')
    
    if request.method == "POST":
        action = request.form['action']
        row_id = request.form['row_id']
        
        if action == 'view':
            session['row_id'] = row_id
            print(row_id)
            return redirect(url_for('face_scan'))
        
    cursor = dtb.cursor()
    cursor.execute("SELECT * FROM attendance_checked WHERE classroom_id = %s", (classroom_id,))
    attendances = cursor.fetchall()
    return render_template('/Student/attendance_checking.html', attendances=attendances)

@app.route('/face_scan', methods=['GET', 'POST'])
def face_scan():
    student_id = session.get('student_id')
    if not student_id:
        flash("Please log in to access this feature.")
        return redirect(url_for('homepage'))
    return render_template('/Student/facescan.html')

@app.route('/video_feed')
def video_feed():
    student_id = session.get('student_id')
    if not student_id:
        flash("Please log in to access this feature.")
        return redirect(url_for('homepage'))
    try:
        # Stream video feed
        return Response(generate_frames(student_id), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        # Log the error and show a user-friendly message
        print(f"Error in video feed: {e}")
        flash("An error occurred while accessing the video feed. Please try again later.", "danger")
        return redirect(url_for('face_scan'))

mode = 'dev'

if __name__ == '__main__':
    if mode == 'dev':
        app.run(debug=True)
    else:
        serve(app, host='0.0.0.0', port=5000, threads=2, url_prefix="/attendance-management")