import json, re, random

def preprocess_input(input_text):
    # Tokenize and preprocess the input by converting to lowercase and removing punctuation
    return re.sub(r'[^\w\s]', '', input_text.lower()).split()

def identify_intent(input_tokens, intents_data):
    # Iterate through each intent and its patterns
    for intent in intents_data["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = preprocess_input(pattern)
            # Check if the input_tokens contain all the tokens in the pattern
            if all(token in input_tokens for token in pattern_tokens):
                return intent["tag"], intent["follow_up_questions"]

    # If no intent is matched, return a default intent
    return "default", []

# Load the intents data from intents.json
with open("mysite/chatbotFiles/intents.json", "r") as file:
    intents_data = json.load(file)

def get_response(intent_tag):
    # Get the appropriate response for the identified intent
    for intent in intents_data["intents"]:
        if intent["tag"] == intent_tag:
            response = intent["responses"]
            return response
            break

# If there are follow-up questions, ask them
#if follow_up_questions:
#    for question in follow_up_questions:
#        user_response = input("Bot: " + question + " ")
#        # Process user's response to follow-up questions as needed

def get_cr_ev_followup_questions():
    cr_ev_followup_questions = ['What do you want your Event Title to be?', 
                                'What is the Date for this Event?', 
                                'What is the start time for this event? Include AM/PM', 
                                'What is the end time for this event? Include AM/PM', 
                                'You can customize your event more in a few seconds...']
    return cr_ev_followup_questions

def get_help_login_followup_questions():
    help_login_followup_questions = [
            "What is your email?",
            "What is your password?"
        ]
    return help_login_followup_questions

def get_intent_tag(message):
    input_tokens = preprocess_input(message)
    intent_tag, follow_up_questions = identify_intent(input_tokens, intents_data)
    return intent_tag

def user_input(message, page):
    intent_tag = get_intent_tag(message)
    if page != 'login_page':
        if intent_tag != 'create_event' and intent_tag != 'default':
            possible_responses = get_response(intent_tag)
            return random.choice(possible_responses)
        else:
            return 'null'
    elif page == 'login_page':
        if intent_tag == 'create_event':
            return "You can only create events after you have logged in to your home page"
        if intent_tag == 'help':
            return "I can only assist you with logging in. Type 'log in' for my assistance"
        elif intent_tag == 'default':
            return "null"
        else:
            possible_responses = get_response(intent_tag)
            return random.choice(possible_responses)
        