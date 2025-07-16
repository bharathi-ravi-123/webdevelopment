# Final version after resolving conflict
print("This is local code with additional remote feature")


from flask import Flask , render_template ,  request , redirect , url_for , flash
import mysql.connector
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash , check_password_hash
from flask import session
from flask import jsonify


app = Flask(__name__)
app.secret_key = 's1b8@5400#we'



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ravibharathi0108@gmail.com'      
app.config['MAIL_PASSWORD'] = 'hiqh sxfw xjwm mukl'                              
app.config['MAIL_DEFAULT_SENDER'] = 'ravibharathi0108@gmail.com'  

mail = Mail(app)

#def mask_password(password):
#   if len(password) < 4:
#       return '*' * len(password)
#   return password[0] + '*' * (len(password) - 4) + password[-3:]


db = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="rootadmin123",
    database="registerdb"
)

cursor = db.cursor(dictionary=True)
   


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register' , methods=['GET' , 'POST'])

def register(): 
    if request.method == 'POST':
        username = request.form.get('fname', '').strip()
        email = request.form.get('mail', '').strip()
        password = request.form.get('passw', '').strip()

        if not username or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for('index'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("Email already registered!", "error")
            return redirect(url_for('login'))
        else:
            sql = "INSERT INTO students (username, email, password) VALUES (%s, %s, %s)"
            values = (username, email, hashed_password)
            cursor.execute(sql, values)
            db.commit()

            #masked = password[0] + '*' * (len(password) - 4) + password[-3:] if len(password) >= 4 else '*' * len(password)

            user_msg = Message("Welcome! Registration Successful", recipients=[email])
            user_msg.body = f"""
            Hello {username},

            You have registered successfully.

            Username: {username}
            Password: {password}

            Keep this info safe.
            """

            admin_email = "ravibharathi0108@gmail.com"
            admin_msg = Message("New User Registered", recipients=[admin_email])
            admin_msg.body = f"""
            A new user has registered:

            Name: {username}
            Email: {email}
            """

            try:
                mail.send(user_msg)
                mail.send(admin_msg)
                print("Admin email sent!")
            except Exception as e:
                flash("Email sending failed (registration was saved).", "error")
                print("Email sending failed:", e)

            flash("Registration successful", "success")
            return redirect(url_for('login')) 

    
    cursor.execute("SELECT email FROM students")
    emails = [email['email'] for email in cursor.fetchall()]
    return render_template("register.html", registered_emails=emails)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('pass').strip()

        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            flash("Email not registered. Please register first.", "error")
            return redirect(url_for('register'))

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['email']
            flash("Login successful", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect email or password", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', email=session['user_id'])
    else:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('login'))
    

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        flash("Your message has been sent!", "success")
        
    return render_template('contact.html')


@app.route('/payment')
def payment():
    course = request.args.get('course', '')
    course_prices = {
        "Web Development": 4599,
        "UI & UX Design": 3999,
        "AIML": 5999,
        "Digital Marketing": 1999,
        "Cyber Security": 1299,
        "Data Science": 5999,
        "Power BI": 1599,
        "Advance Python": 1999,
        "Deep Learning": 7999
    }
    price = course_prices.get(course, 0)
    return render_template('payment.html', course=course, price=price)



@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))


@app.route('/success')
def success():
    return render_template('success.html')


@app.route("/store_payment", methods=["POST"])
def store_payment():
    print("store_payment called")
    data = request.get_json()
    print("Received payment data:", data)

    payment_id = data.get("payment_id")
    course = data.get("course")
    name = data.get("name")
    email = data.get("email")

    if not all([payment_id, course, name, email]):
        print("Missing data in payment request")
        return jsonify({"error": "Missing data"}), 400

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO payments (payment_id, course, name, email) VALUES (%s, %s, %s, %s)",
            (payment_id, course, name, email)
        )
        db.commit()
        print("Payment record inserted into database")
    except Exception as e:
        db.rollback()
        print("Database error:", e)
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    user_msg = Message(
        subject="✅ Payment Confirmation - Tagore Engineering",
        recipients=[email],
        body=f"""
Dear {name},

Thank you for registering for the course: {course}.

Your payment has been successfully received.
Payment ID: {payment_id}

Your sessions will start from 20th August

We look forward to your participation!

Best regards,
Tagore Engineering College
"""
    )

    admin_msg = Message(
        subject=f"New Course Registration - {name}",
        recipients=["ravibharathi0108@gmail.com"],
        body=f"""
New registration received:

Name: {name}
Email: {email}
Course: {course}
Payment ID: {payment_id}
"""
    )

    try:
        print(f"Sending payment confirmation email to user: {email}")
        mail.send(user_msg)
        print("User payment email sent successfully")
    except Exception as e:
        print(f"Error sending user payment email: {e}")

    try:
        print("Sending notification email to admin")
        mail.send(admin_msg)
        print("Admin notification email sent successfully")
    except Exception as e:
        print(f"Error sending admin notification email: {e}")

    return jsonify({"message": "Payment saved and emails sent (if no errors)."}), 200



if __name__ == '__main__':
=======

from flask import Flask , render_template ,  request , redirect , url_for , flash
import mysql.connector
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash , check_password_hash
from flask import session
from flask import jsonify


app = Flask(__name__)
app.secret_key = 's1b8@5400#we'



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ravibharathi0108@gmail.com'      
app.config['MAIL_PASSWORD'] = 'hiqh sxfw xjwm mukl'                              
app.config['MAIL_DEFAULT_SENDER'] = 'ravibharathi0108@gmail.com'  

mail = Mail(app)

#def mask_password(password):
#   if len(password) < 4:
#       return '*' * len(password)
#   return password[0] + '*' * (len(password) - 4) + password[-3:]


db = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="rootadmin123",
    database="registerdb"
)

cursor = db.cursor(dictionary=True)
   


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register' , methods=['GET' , 'POST'])

def register(): 
    if request.method == 'POST':
        username = request.form.get('fname', '').strip()
        email = request.form.get('mail', '').strip()
        password = request.form.get('passw', '').strip()

        if not username or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for('index'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("Email already registered!", "error")
            return redirect(url_for('login'))
        else:
            sql = "INSERT INTO students (username, email, password) VALUES (%s, %s, %s)"
            values = (username, email, hashed_password)
            cursor.execute(sql, values)
            db.commit()

            #masked = password[0] + '*' * (len(password) - 4) + password[-3:] if len(password) >= 4 else '*' * len(password)

            user_msg = Message("Welcome! Registration Successful", recipients=[email])
            user_msg.body = f"""
            Hello {username},

            You have registered successfully.

            Username: {username}
            Password: {password}

            Keep this info safe.
            """

            admin_email = "ravibharathi0108@gmail.com"
            admin_msg = Message("New User Registered", recipients=[admin_email])
            admin_msg.body = f"""
            A new user has registered:

            Name: {username}
            Email: {email}
            """

            try:
                mail.send(user_msg)
                mail.send(admin_msg)
                print("Admin email sent!")
            except Exception as e:
                flash("Email sending failed (registration was saved).", "error")
                print("Email sending failed:", e)

            flash("Registration successful", "success")
            return redirect(url_for('login')) 

    
    cursor.execute("SELECT email FROM students")
    emails = [email['email'] for email in cursor.fetchall()]
    return render_template("register.html", registered_emails=emails)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('pass').strip()

        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            flash("Email not registered. Please register first.", "error")
            return redirect(url_for('register'))

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['email']
            flash("Login successful", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect email or password", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', email=session['user_id'])
    else:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('login'))
    

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        flash("Your message has been sent!", "success")
        
    return render_template('contact.html')


@app.route('/payment')
def payment():
    course = request.args.get('course', '')
    course_prices = {
        "Web Development": 4599,
        "UI & UX Design": 3999,
        "AIML": 5999,
        "Digital Marketing": 1999,
        "Cyber Security": 1299,
        "Data Science": 5999,
        "Power BI": 1599,
        "Advance Python": 1999,
        "Deep Learning": 7999
    }
    price = course_prices.get(course, 0)
    return render_template('payment.html', course=course, price=price)



@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))


@app.route('/success')
def success():
    return render_template('success.html')


@app.route("/store_payment", methods=["POST"])
def store_payment():
    print("store_payment called")
    data = request.get_json()
    print("Received payment data:", data)

    payment_id = data.get("payment_id")
    course = data.get("course")
    name = data.get("name")
    email = data.get("email")

    if not all([payment_id, course, name, email]):
        print("Missing data in payment request")
        return jsonify({"error": "Missing data"}), 400

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO payments (payment_id, course, name, email) VALUES (%s, %s, %s, %s)",
            (payment_id, course, name, email)
        )
        db.commit()
        print("Payment record inserted into database")
    except Exception as e:
        db.rollback()
        print("Database error:", e)
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    user_msg = Message(
        subject="✅ Payment Confirmation - Tagore Engineering",
        recipients=[email],
        body=f"""
Dear {name},

Thank you for registering for the course: {course}.

Your payment has been successfully received.
Payment ID: {payment_id}

Your sessions will start from 20th August

We look forward to your participation!

Best regards,
Tagore Engineering College
"""
    )

    admin_msg = Message(
        subject=f"New Course Registration - {name}",
        recipients=["ravibharathi0108@gmail.com"],
        body=f"""
New registration received:

Name: {name}
Email: {email}
Course: {course}
Payment ID: {payment_id}
"""
    )

    try:
        print(f"Sending payment confirmation email to user: {email}")
        mail.send(user_msg)
        print("User payment email sent successfully")
    except Exception as e:
        print(f"Error sending user payment email: {e}")

    try:
        print("Sending notification email to admin")
        mail.send(admin_msg)
        print("Admin notification email sent successfully")
    except Exception as e:
        print(f"Error sending admin notification email: {e}")

    return jsonify({"message": "Payment saved and emails sent (if no errors)."}), 200



if __name__ == '__main__':
>>>>>>> 4289f13b43258df81e2568ab5429a9b373c6868a
 app.run(debug=True)