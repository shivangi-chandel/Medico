from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask import g
import os
import hashlib
from flask import Flask, render_template, jsonify
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import MySQLdb.cursors

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


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin_id, password FROM admins WHERE username = %s", (username,))
        admin = cursor.fetchone()
        
        if admin and admin[1] == password:  
            session['admin_id'] = admin[0]  # Store the admin ID in the session
            flash("Login successful!", "success")
            return redirect(url_for('admin'))
        else:
            flash("Invalid credentials!", "danger")
    
    return render_template('admin_login.html')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('admin_login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))  # Redirect to admin login page
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Fetch patient profile data
    cursor.execute("SELECT * FROM patient_profiles")
    patient_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM doctors ")
    doctor_data = cursor.fetchall()
    
    error_message = {}
    if request.method == 'POST':
        # Determine which form was submitted based on a hidden input field
        form_type = request.form.get('form_type')
        
        if form_type == 'add_department':
            # Add Department Form Logic
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
            return redirect(url_for('admin'))  # Redirect to admin page

        elif form_type == 'add_category':
            # Add Category Form Logic
            name = request.form['name']
            description = request.form.get('description', '')
            price = request.form['price']
            icon = request.files.get('icon')
            # Convert price to float or int
            try:
              price = int(price)  # Use float for decimal prices, or int if you want to restrict it to whole numbers
            except ValueError:
              error_message['price'] = "Invalid price format! Please enter a valid number."
              return render_template('admin.html', error_message=error_message)
            
            # Check if category already exists
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM categories WHERE name = %s', (name,))
            existing_category = cursor.fetchone()
            if existing_category:
                error_message['category_name'] = "Category with this name already exists!"
                return render_template('admin.html', error_message=error_message)
            
            
            # Validate icon file extension
            if icon and allowed_file(icon.filename):
                # Save icon if valid format (png or svg)
                icon_filename = secure_filename(icon.filename)
                icon_path = os.path.join(app.config['UPLOAD_FOLDER'], 'categories', icon_filename)
                os.makedirs(os.path.dirname(icon_path), exist_ok=True)
                icon.save(icon_path)
                icon_url = f'/{icon_path}'  # Relative URL for uploaded file
            else:
                error_message['category_icon'] = "Only PNG and SVG file formats are allowed!"
                return render_template('admin.html', error_message=error_message)

            
            # Insert category into MySQL database
            cursor.execute('''
                INSERT INTO categories (name, description, price, icon_url, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            ''', (name, description, price, icon_url))
            mysql.connection.commit()
            cursor.close()

            flash("Category added successfully!", "success")
            return redirect(url_for('admin'))  # Redirect to admin page
        
        elif form_type == 'add_test':
            # Add Test Form Logic
            name = request.form['name']
            description = request.form.get('description', '')
            price = request.form['price']
            icon = request.files.get('icon')
            test_type = request.form['test_type'] 
            try:
              price = int(price)  # Use float for decimal prices, or int if you want to restrict it to whole numbers
            except ValueError:
              error_message['price'] = "Invalid price format! Please enter a valid number."
              return render_template('admin.html', error_message=error_message)
            
            # Check if category already exists
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM labTest WHERE test_name = %s', (name,))
            existing_test = cursor.fetchone()
            if existing_test:
                error_message['test_name'] = "Test with this name already exists!"
                return render_template('admin.html', error_message=error_message)
            
            
            # Validate icon file extension
            if icon and allowed_file(icon.filename):
                # Save icon if valid format (png or svg)
                icon_filename = secure_filename(icon.filename)
                icon_path = os.path.join(app.config['UPLOAD_FOLDER'], 'labTest', icon_filename)
                os.makedirs(os.path.dirname(icon_path), exist_ok=True)
                icon.save(icon_path)
                icon_url = f'/{icon_path}'  # Relative URL for uploaded file
            else:
                error_message['test_icon'] = "Only PNG and SVG file formats are allowed!"
                return render_template('admin.html', error_message=error_message)

            
            # Insert category into MySQL database
            cursor.execute('''
                INSERT INTO labTest (test_name, description, test_price, type, icon_url)
                VALUES (%s, %s, %s, %s ,%s)
            ''', (name, description, price, test_type,icon_url))
            mysql.connection.commit()
            cursor.close()

            flash("lab test added successfully!", "success")
            return redirect(url_for('admin'))  # Redirect to admin page

    return render_template('admin.html', error_message=error_message,patients=patient_data,doctors=doctor_data)

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM patient_profiles WHERE patient_id = %s", (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        flash("Patient not found!", "danger")
        return redirect(url_for('admin'))  # Redirect to the patient list page

    if request.method == 'POST':
        full_name = request.form["full_name"]
        contact_number = request.form["contact_number"]
        email = request.form["email"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        age = request.form["age"]
        status = request.form["status"]

        query = """
            UPDATE patient_profiles 
            SET full_name = %s, contact_number = %s, email = %s, dob = %s, 
                gender = %s, age = %s, status = %s
            WHERE patient_id = %s
        """
        values = (full_name, contact_number, email, dob, gender, age, status, patient_id)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        
        flash("Patient updated successfully!", "success")
        return redirect(url_for('patient_list'))  # Redirect after updating

    return render_template('edit_patient.html', patient=patient)

@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    if 'admin_id' not in session:
        flash("Access denied! Please log in as an admin.", "danger")
        return redirect(url_for('admin_login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM patient_profiles WHERE patient_id = %s", (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        flash("Patient not found!", "danger")
        return redirect(url_for('admin'))

    # Delete patient record from database
    cursor.execute("UPDATE patient_profiles SET status = %s WHERE patient_id = %s", ("Inactive", patient_id))
    mysql.connection.commit()
    cursor.close()

    flash("Patient deleted successfully!", "success")
    return redirect(url_for('admin'))

@app.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    if 'admin_id' not in session:
        flash("Access denied! Please log in as an admin.", "danger")
        return redirect(url_for('admin_login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,))
    patient = cursor.fetchone()

    if not patient:
        flash("Patient not found!", "danger")
        return redirect(url_for('admin'))

    # Delete patient record from database
    cursor.execute("UPDATE doctors SET status = %s WHERE doctor_id = %s", ("Inactive", doctor_id))
    mysql.connection.commit()
    cursor.close()

    flash("Doctor deleted successfully!", "success")
    return redirect(url_for('admin'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error message variable

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password, role FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        if user is None:  # Handle the case when no user is found
            error = "Invalid email or password. Please try again."
            return render_template('login.html', error=error)

        if password==user[2]:  # Verify hashed password
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]

            if user[3] == 'doctor':
                return redirect('/doctor_dashboard')
            else:
                return redirect('/')
        else:
            error = "Invalid email or password. Please try again."

    return render_template('login.html', error=error)

    
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    flash("Logged out successfully!", "success")
    return redirect('/')  # Redirect to login page


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        contact_number = request.form['phone_number']
        password = request.form['password']
        role = request.form['role']
        
        # Check if email or phone number already exists
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s OR contact_number = %s', (email, contact_number))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email or phone number already exists!", "danger")
            return render_template('register.html')

        # Insert new user into the users table
        cursor.execute('''
            INSERT INTO users (username, email, contact_number, password ,role)
            VALUES (%s, %s, %s, %s ,%s)
        ''', (username, email, contact_number, password,role))
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
    # Fetch all categories from MySQL database
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT * FROM categories')
      categories = cursor.fetchall()    
      cursor.close()
    
      return render_template('consultation.html',categories=categories)
  
@app.route('/doctors', defaults={'category_id': None})
@app.route('/doctors/<int:category_id>')
def doctors(category_id):
    cursor = mysql.connection.cursor()

    if category_id:
        # Fetch doctors for the given category
        cursor.execute("SELECT doctor_id, full_name, specialization, experience, fees, profile_picture FROM doctors WHERE category_id = %s", (category_id,))
    else:
        # Fetch all doctors
        cursor.execute("SELECT doctor_id, full_name, specialization, experience, fees, profile_picture FROM doctors")

    doctors = cursor.fetchall()
    cursor.close()

    return render_template('doctors.html', doctors=doctors, category_id=category_id)


@app.route('/lab')
def lab():
    cursor = mysql.connection.cursor()

    # Fetch tests based on type
    cursor.execute("SELECT * FROM labTest WHERE type = 'Top Test'")
    top_tests = cursor.fetchall()
    
    cursor.execute("SELECT * FROM labTest WHERE type = 'Daily Routine'")
    daily_routine_tests = cursor.fetchall()

    cursor.execute('SELECT * FROM labTest')
    labTests = cursor.fetchall()    
   
    cursor.execute("SELECT * FROM labTest WHERE type = 'Women Care'")
    women_care_tests = cursor.fetchall()

    cursor.close()
    return render_template('lab.html', top_tests=top_tests, daily_routine_tests=daily_routine_tests,  labTests=labTests, women_care_tests=women_care_tests)


@app.route("/book_appointment")
def appointment():
    # Render the page where the user can book the appointment
    return render_template("book_appointment.html")

# Profile Restriction Decorator for Doctors
from functools import wraps

def profile_required(f):
    @wraps(f)  # This preserves the original function name
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM doctors WHERE account_id = %s", (session['user_id'],))
        g.doctor = cursor.fetchone()
        cursor.close()

        if not g.doctor:
            return redirect(url_for('complete_profile'))

        return f(*args, **kwargs)

    return decorated_function

# Doctor Dashboard Route (Requires Profile Completion)
@app.route('/doctor_dashboard')
@profile_required
def doctor_dashboard():
    return render_template('doctor_dashboard.html', doctor=g.doctor)

#  Profile Completion Route
@app.route('/doctor-detail', methods=['GET', 'POST'])
def complete_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

   # Fetch user details (email & contact_number from users table)
    cursor.execute("SELECT id, username, email, contact_number FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone() 
    user_data = {'user_id': user[0], 'name': user[1], 'email': user[2], 'phone': user[3]} if user else None

    # Fetch doctor details (if profile exists)
    cursor.execute("SELECT * FROM doctors WHERE account_id = %s", (session['user_id'],))
    doctor_data = cursor.fetchone()
    
    # Fetch categories from database
    cursor.execute("SELECT category_id, name, price FROM categories")
    categories = cursor.fetchall()
    categories = [{'category_id': cat[0], 'name': cat[1], 'price': cat[2]} for cat in categories]


    fees = ""  # Default empty fees
    selected_category_id = None  # To track selected category
            
    if request.method == 'POST':
        selected_category_id = request.form["category_id"]  # Get selected category

        # Fetch fees for the selected category
        cursor.execute("SELECT price FROM categories WHERE category_id = %s", (selected_category_id,))
        category_fee = cursor.fetchone()
        if category_fee:
            fees = category_fee[0]  # Assign the fee to be displayed

        
        full_name = request.form["full_name"]
        specialization = request.form["specialization"]
        experience = request.form["experience"]
        category_id = request.form["category_id"]
        contact_number = request.form["contact_number"]
        email = request.form["email"]
        status = request.form["status"]
        
        # Handle Profile Picture Upload
        profile_picture = request.files['profile_picture']
        picture_path = doctor_data['profile_picture'] if doctor_data else None  # Keep old picture if not updating

        if profile_picture and profile_picture.filename:
            filename = secure_filename(f"{session['user_id']}_{profile_picture.filename}")
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            picture_path = f'/static/uploads/{filename}'

        # If doctor exists, update profile
        if doctor_data:
            query = """
                UPDATE doctors 
                SET full_name = %s, specialization = %s, contact_number = %s,
                    email = %s, category_id = %s, status = %s, profile_picture = %s
                WHERE account_id = %s
            """
            values = (full_name, specialization, contact_number, email, category_id, status, picture_path, session['user_id'])
            cursor.execute(query, values)
        else:
            # Insert new profile
            cursor.execute("""
            INSERT INTO doctors (full_name, specialization, experience, category_id, fees, 
                                contact_number, email, profile_picture, account_id, status, registration_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (full_name, specialization, experience, category_id, fees, contact_number, email,picture_path, session['user_id'], status))
        mysql.connection.commit()
        cursor.close()

        flash('Profile saved successfully!', 'success')
        return redirect(url_for('doctor_dashboard'))

    cursor.close()
    
    # Pre-fill form with existing data
    return render_template('doctor-detail.html', user=user_data, doctor=doctor_data, categories=categories, fees=fees, selected_category_id=selected_category_id)


# Route to Book Appointment
@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    try:
        data = request.json  # Get JSON data from request
        doctor_id = data.get("doctor_id")
        patient_id = data.get("patient_id")
        date = data.get("date")
        time = data.get("time")
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

        # Return a JSON response after successful booking
        return jsonify({"success": True, "message": "Appointment booked successfully!"})

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"success": False, "message": str(e)}), 500  # Return error response



# Custom Login Required Decorator
def login_required_customm(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to log in first!", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/profile')
@login_required_customm
def profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Fetch patient profile data
    cursor.execute("SELECT * FROM patient_profiles WHERE patient_id = %s", (session['user_id'],))
    patient_data = cursor.fetchone()

    # Redirect if profile is incomplete
    if not patient_data or not all([patient_data.get('full_name'), patient_data.get('contact_number'), patient_data.get('email')]):
        return redirect(url_for('patient_form'))

    # Fetch patient's booking details
    cursor.execute("""
        SELECT b.id, b.date, b.time, b.room_name, d.full_name AS doctor_name 
        FROM bookings b
        JOIN doctors d ON b.doctor_id = d.doctor_id
        WHERE b.patient_id = %s
        ORDER BY b.date DESC
    """, (session['user_id'],))
    
    bookings = cursor.fetchall()
    cursor.close()

    return render_template('profile.html', patient=patient_data, bookings=bookings)


@app.route('/patient_form', methods=['GET', 'POST'])
@login_required_customm
def patient_form():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    user_data={'user_id': user[0], 'name': user[1], 'email': user[2], 'phone': user[4]} if user else None
    cursor.execute("SELECT * FROM patient_profiles WHERE patient_id = %s", (session['user_id'],))
    patient_data = cursor.fetchone()
    print("Request Method:", request.method)  # Debugging
    print("Request Form Data:", request.form)  # Debugging
    
    if request.method == 'POST':
        

        if not request.form:
            flash("Form submission failed!", "danger")
            return redirect(url_for('patient_form'))
        
        full_name = request.form["full_name"]
        contact_number = request.form["contact_number"]
        email = request.form["emailaddress"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        blood_group = request.form["blood_group"]
        allergies = request.form["allergies"]
        chronic_conditions = request.form["chronic_conditions"]
        current_medications = request.form["current_medications"]
        emergency_contact_name= request.form["emergency_contact_name"]
        emergency_contact_number= request.form["emergency_contact_number"]
        insurance_provider= request.form["insurance_provider"]
        policy_number= request.form["policy_number"]
        insurance_expiry_date= request.form["insurance_expiry_date"]
        age = int(request.form["age"])
        height_feet = int(request.form["height_feet"])
        height_inch = int(request.form["height_inches"])
        weight = int(request.form["weight"])
        address = request.form["street_address"]
        city = request.form["city"]
        state = request.form["state"]   
            
        profile_picture = request.files['profile_picture']
        picture_path = patient_data['profile_picture'] if patient_data else None  # Keep old picture if not updating

        if profile_picture and profile_picture.filename:
            filename = secure_filename(f"{session['user_id']}_{profile_picture.filename}")
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            picture_path = f'/static/uploads/{filename}'


        if patient_data:
            query = """
                UPDATE patient_profiles 
                SET full_name = %s, contact_number = %s, email = %s, dob = %s, gender = %s, 
                    blood_group = %s, allergies = %s, chronic_conditions = %s, 
                    current_medications = %s, emergency_contact_name = %s, emergency_contact_number = %s, 
                    insurance_provider = %s, policy_number = %s, insurance_expiry_date = %s, 
                    profile_picture = %s, registration_date = NOW(), age = %s, height_feet = %s, height_inch = %s, weight = %s, address = %s, city = %s, state = %s
                WHERE patient_id = %s
                """
            values = (full_name, contact_number, email, dob, gender, blood_group, allergies, chronic_conditions, 
                    current_medications, emergency_contact_name, emergency_contact_number, insurance_provider, 
                    policy_number, insurance_expiry_date, picture_path, age, height_feet, height_inch, weight, address, city, state, session['user_id'])
        else:
            query = """
                    INSERT INTO patient_profiles 
                    (full_name, contact_number, email, patient_id, dob, gender, blood_group, allergies, 
                    chronic_conditions, current_medications, emergency_contact_name, emergency_contact_number, 
                    insurance_provider, policy_number, insurance_expiry_date, profile_picture, registration_date, 
                    age, height_feet, height_inch, weight, address, city, state)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s)
                    """
            values = (full_name, contact_number, email, session['user_id'], dob, gender, blood_group, allergies, 
                    chronic_conditions, current_medications, emergency_contact_name, emergency_contact_number, 
                    insurance_provider, policy_number, insurance_expiry_date, picture_path, age, height_feet, 
                    height_inch, weight, address, city, state)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        print("Request method:", request.method)  # Should print "POST"
        print(request.form)  # Should contain submitted data
        return redirect(url_for('profile'))

    return render_template('patient_form.html', patient=patient_data, user=user_data)



@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Route to Start Video Call
@app.route("/video-call")
def video_call():
    room_name = request.args.get("room_name")
    return render_template("video_call.html", room_name=room_name)

if __name__ == '__main__':
    app.run(debug=True)

