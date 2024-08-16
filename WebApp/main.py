from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length
import requests
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
def login():
    if request.method == 'POST':
        email = request.form['Email address']
        password = request.form['password']
        role = request.form['role']
        
        cursor = user_auth.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s AND role=%s", (email, password, role))
        
        account = cursor.fetchone()
        
        if account:
            return redirect(url_for('Lecturers'))
        else:
            flash('Incorrect login credentials. Please try again.')
    
    return render_template("homepage.html")
    
    
@app.route('/Lecturers')
def lecturers():
    return render_template("Lecturers.html")

if __name__ == '__main__':
    app.run(debug=True)
    