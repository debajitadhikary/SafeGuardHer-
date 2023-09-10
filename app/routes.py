from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt  # Uncomment these lines
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask import jsonify
from flask_login import login_user, logout_user, login_required, current_user

# Home Page
@app.route("/")
def home():
    return render_template('home.html', title='Home')




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Initialize the registration form

    if form.validate_on_submit():  # Check if the form was submitted and is valid
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if the username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email address already registered. Please use a different email.', 'danger')
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)  # Pass the form to the template





@app.route('/rights')
def rights():
    return render_template('rights.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()  # Create a login form (you need to define this form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
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