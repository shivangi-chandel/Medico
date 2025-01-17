from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import os
import hashlib
from flask import Flask, render_template, jsonify
import uuid


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'svg'}  # Allowed file extensions
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Update with your MySQL password
app.config['MYSQL_DB'] = 'medico'  # The name of your database

# Initialize MySQL
mysql = MySQL(app)

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    error_message = {}
    
    if request.method == 'POST':
        department_id = request.form['departmentId']
        department_name = request.form['departmentName']
        department_title = request.form['departmentTitle']
        picture = request.files['departmentPicture']

        # Check if department already exists
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Department WHERE department_name = %s', (department_name,))
        existing_department = cursor.fetchone()
        if existing_department:
            error_message['department_name'] = "Department with this name already exists!"
            return render_template('admin.html', error_message=error_message)

        # Validate picture file extension
        if picture and allowed_file(picture.filename):
            # Save picture if valid format (png or svg)
            picture_filename = os.path.join(app.config['UPLOAD_FOLDER'], picture.filename)
            picture.save(picture_filename)
        else:
            error_message['department_picture'] = "Only PNG and SVG file formats are allowed!"
            return render_template('admin.html', error_message=error_message)

        # Insert department into MySQL database
        cursor.execute('''
            INSERT INTO Department (department_id, department_name, department_title, picture)
            VALUES (%s, %s, %s, %s)
        ''', (department_id, department_name, department_title, picture_filename))
        mysql.connection.commit()
        cursor.close()

        flash("Department added successfully!", "success")

    return render_template('admin.html', error_message=error_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))  # If already logged in, redirect to admin page

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the entered password and check against database
        hashed_password = hash_password(password)

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, hashed_password))
        user = cursor.fetchone()
        
        if user:
            session['username'] = username  # Store username in session
            flash("Login successful!", "success")
            return redirect(url_for('index'))  # Redirect to admin page
        else:
            flash("Invalid username or password", "danger")
            return render_template('login.html')  # Reload login page

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))  # Redirect to login page


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        
        # Check if email or phone number already exists
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s OR phone_number = %s', (email, phone_number))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email or phone number already exists!", "danger")
            return render_template('register.html')

        # Hash the password
        hashed_password = hash_password(password)

        # Insert new user into the users table
        cursor.execute('''
            INSERT INTO users (username, email, phone_number, password)
            VALUES (%s, %s, %s, %s)
        ''', (username, email, phone_number, hashed_password))
        mysql.connection.commit()
        cursor.close()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))  # Redirect to login page

    return render_template('register.html')

@app.route('/')
def index():
    # Fetch all departments from MySQL database
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Department')
    departments = cursor.fetchall()
    cursor.close()
    
    return render_template('index.html', departments=departments)

@app.route('/consultation')
def consultation():
    return render_template('consultation.html')

@app.route('/lab')
def lab():
    return render_template('lab.html')

@app.route("/book_appointment")
def appointment():
    # Render the page where the user can book the appointment
    return render_template("book_appointment.html")

# Route to Book Appointment
@app.route("/book-appointment", methods=["GET", "POST"])
def book_appointment():
    if request.method == "POST":
        doctor_id = request.form["doctor_id"]
        patient_id = request.form["patient_id"]
        date = request.form["date"]
        time = request.form["time"]
        room_name = f"MedicoRoom-{uuid.uuid4().hex[:8]}"  # Generate unique room name

        # Save booking in the database
        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            INSERT INTO bookings (doctor_id, patient_id, date, time, room_name)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (doctor_id, patient_id, date, time, room_name)
        )
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("consultation"))  # Redirect back to the index page
    return render_template("book_appointment.html")


# Route to View Appointments
@app.route("/view-appointments/<user_type>/<user_id>")
def view_appointments(user_type, user_id):
    cursor = mysql.connection.cursor()

    if user_type == "doctor":
        cursor.execute(
            """
            SELECT b.booking_id, p.name AS patient_name, b.date, b.time, b.room_name
            FROM bookings b
            JOIN patients p ON b.patient_id = p.patient_id
            WHERE b.doctor_id = %s
            """, (user_id,)
        )
    elif user_type == "patient":
        cursor.execute(
            """
            SELECT b.booking_id, d.name AS doctor_name, b.date, b.time, b.room_name
            FROM bookings b
            JOIN doctors d ON b.doctor_id = d.doctor_id
            WHERE b.patient_id = %s
            """, (user_id,)
        )
    
    appointments = cursor.fetchall()
    cursor.close()
    return render_template("view_appointments.html", appointments=appointments, user_type=user_type)


# Route to Start Video Call
@app.route("/video-call")
def video_call():
    room_name = request.args.get("room_name")
    return render_template("video_call.html", room_name=room_name)

if __name__ == '__main__':
    app.run(debug=True)
