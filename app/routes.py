from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt  # Uncomment these lines
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask import jsonify

# Home Page
@app.route("/")
def home():
    return render_template('home.html', title='Home')

# User Registration
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# User Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log in the user using Flask-Login
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

# Sending an Emergency Signal
@app.route("/emergency", methods=['GET', 'POST'])
def emergency():
    if request.method == 'POST':
        # Add code for sending the signal to nearby responders
        flash('Emergency signal sent. Help is on the way.', 'success')
        return redirect(url_for('emergency'))
    return render_template('emergency.html', title='Emergency Signal')



# ...

# New route to handle emergency signal
@app.route("/send_emergency_signal", methods=['POST'])
def send_emergency_signal():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Add code to send the emergency signal with the received latitude and longitude
    # You can use a third-party service or any other method to send the SOS

    return jsonify(message="Emergency signal received and being processed")