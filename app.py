from flask import Flask, request, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'temporary_key'

def get_db_connection():
    return mysql.connector.connect(
        host='nm2024tmid13862-db.c5s6yoem87dv.us-east-1.rds.amazonaws.com',
        user='admin',
        password='ARUNKARTHIC',
        database=' NM2024TMID13862_DB'
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            (username, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result and check_password_hash(result[0], password):
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')


# Dashboard Route (after login)
@app.route('/dashboard')
def dashboard():
    course_urls = [
        'https://nm2024tmid13862bucket.s3.us-east-1.amazonaws.com/Introduction+to+machine+learning.pdf',
        'https://nm2024tmid13862bucket.s3.us-east-1.amazonaws.com/Python_program.pdf'
    ]
    
    return render_template('dashboard.html', course_urls=course_urls)

# Home Route (Landing Page)

@app.route('/')

def home():

    return render_template('home.html')



# Logout

@app.route('/logout')

def logout():

    return redirect(url_for('login'))



if __name__ == '_main_':

    app.run(host="0.0.0.0", port=5000,debug=True)
