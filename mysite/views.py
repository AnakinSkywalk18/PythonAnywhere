from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user


from mysite.chatbotFiles.chatbot import get_intent_tag, user_input

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    #We will be able to reference the current user and check if user is authenticated
    return render_template("home.html", user=current_user)


@views.post("/predict")
@login_required
def predict():
    text = request.get_json().get("message")
    text = text.lower()
    #Have a function in chatbot.py called get_intent_tag
    #Have an indepentet variable that checks if the intent_tag is create_event

    user_intent_tag = get_intent_tag(text)
    
    if user_intent_tag == 'create_event':
        #Then manually send requests from here and formualte a dictionary... with other python functions too!
        message = {"answer": " "}
        return jsonify(message)
    else:    
        response = user_input(text)
        message = {"answer": response}
        return jsonify(message)