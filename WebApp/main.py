from flask import Flask, render_template, redirect, url_for, request, flash
import mysql.connector


app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"

user_auth = mysql.connector.connect(
    host="127.0.0.1",  # The IP address of the MySQL server
    user="root",       # The username for the database
    password="super123",       # The password for the database (if any, otherwise leave it empty)
    database="user_auth"  # The database name you want to use
)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['choice']
        
        cursor = user_auth.cursor(dictionary=True)

        # Query the database to verify the credentials
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s AND role = %s", (email, password, role))
        user = cursor.fetchone()


        if user:
            # If credentials match, render the appropriate template based on the role
            if role == 'Lecturer':
                return redirect(url_for('lecturers'))
            elif role == 'Student':
                return render_template('#')
        else:
            # If credentials don't match, flash an error message and redirect to homepage
            flash('Invalid credentials, please try again.')
            return redirect(url_for('homepage'))
    return render_template('homepage.html')
    
@app.route('/Lecturers')
def lecturers():
    return render_template("Lecturers.html")

if __name__ == '__main__':
    app.run(debug=True)
    