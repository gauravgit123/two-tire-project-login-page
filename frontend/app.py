from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="db",  # Docker service name for MySQL
        user="root",
        password="admin",
        database="admission_db"
    )

# Home Page (Admission Form)
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admissions')
        admissions = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('dashboard.html', admissions=admissions)
    else:
        return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Submit Admission Form
@app.route('/submit', methods=['POST'])
def submit():
    if 'username' in session:
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO admissions (name, email, course) VALUES (%s, %s, %s)', (name, email, course))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('success'))
    else:
        return redirect(url_for('login'))

# Success Page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
