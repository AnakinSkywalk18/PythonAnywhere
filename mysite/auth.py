import re
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from .models import User
from . import db

from mysite.chatbotFiles.chatbot import get_intent_tag, user_input, get_help_login_followup_questions

us_pass = []

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        button_action = request.form.get('button_action')

        if (button_action == 'signup'):
            flash('Sucessfully brought you to the Sign Up page', category='success')
            return redirect(url_for('auth.sign_up')) 

        else:
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in Successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect Password, try again.', category='error')
            else:
                if(len(email) == 0 and len(password) == 0):
                    flash('Nothing entered. Did you mean to press the Sign Up button?', category='error')
                else:
                    flash('Email does not exist. Please consider signing up on our Sign Up page', category='error')
    return render_template("login.html", user=current_user)

@auth.post("/login/predict") 
def predict(): 
    text = request.get_json().get("message")
    text = text.lower()
    
    if "login_state" not in session:
        message = handle_initial_login_state(text)
    else:
        login_state = session["login_state"]
        if login_state == "prompt_email":
            message = handle_prompt_email_state(text)
        elif login_state == "prompt_password":
            message = handle_prompt_password_state(text)

    return jsonify(message)

def handle_initial_login_state(text):
    user_intent_tag = get_intent_tag(text)
    if user_intent_tag == 'help_log_in':
        session["login_state"] = "prompt_email"
        message = {"answer": "Type in Username"}
    else:
        response = user_input(text, "login_page")
        message = {"answer": response}
    return message

def handle_prompt_email_state(text):
    email = text  # You may want to add some validation for the email
    session["email"] = email
    session["login_state"] = "prompt_password"
    message = {"answer": "Type in Password"}
    return message

def handle_prompt_password_state(text):
    if "password_attempts" not in session:
        session["password_attempts"] = 1
    else:
        session["password_attempts"] += 1

    password_attempts = session.get("password_attempts", 0)

    if password_attempts > 2:
        del session["login_state"]  # Reset the login_state
        del session["password_attempts"]  # Reset the password_attempts
        message = {"answer": "You have exceeded the limit for password attempts. Please start over.", "authenticated": False}
    else:
        password = text
        # Display the email and password entered by the user
        email = session.get("email", None)

        # You can handle the login process here using email and password

        # For example, you can try to authenticate the user and log them in:
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                message = {"answer": "Logged in Successfully!", "authenticated": True}
                if "login_state" in session:
                    del session["login_state"]  # Reset the login_state
                if "password_attempts" in session:
                    del session["password_attempts"]  # Reset the password_attempts
            else:
                #flash('Incorrect Password, try again.', category='error')
                message = {"answer": "Incorrect Password. Please enter the password again.", "authenticated": False}
                session["login_state"] = "prompt_password"  # Prompt for password again

        else:
            #flash('Email does not exist. Please consider signing up on our Sign Up page', category='error')
            message = {"answer": "Email does not exist. Please consider signing up on our Sign Up page", "authenticated": False}
            if "login_state" in session:
                del session["login_state"]  # Reset the login_state

    return message

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 5 or (re.match(email_pattern, email)==False):
            flash('Your email must be greater than 4 characters', category='error')
        elif len(first_name) < 3:
            flash('Your first name must be greater than two characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)