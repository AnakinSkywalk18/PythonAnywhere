class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];

        this.voiceActivationEnabled = false;
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        });

        const toggleButton = document.getElementById('toggle-voice-btn');
        toggleButton.addEventListener('click', () => {
        this.toggleVoiceActivation();
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    //Toggling Voice Activation [On or Off]
    toggleVoiceActivation() {
        this.voiceActivationEnabled = !this.voiceActivationEnabled;
        if (this.voiceActivationEnabled === false)
        {
            alert("Voice Activation is Disabled")
        }
        else if(this.voiceActivationEnabled === true)
        {
            alert("Voice Activation is Enabled")
        }
    }
    
    // Function to speak the chatbot's response
    speakResponse(responseText) {
        if (this.voiceActivationEnabled) {
          const speechSynthesis = window.speechSynthesis;
          const utterance = new SpeechSynthesisUtterance(responseText);
          speechSynthesis.speak(utterance);
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }
    
        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
    
        fetch('http://127.0.0.1:5000/login/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(response => response.json())
          .then(data => {
            // Extract the chatbot's answer from the JSON response
            let chatbotAnswer = data.answer;
            let msg2 = { name: "Cal", message: chatbotAnswer };

            this.speakResponse(chatbotAnswer);

            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = '';
    
            // Check if the user is authenticated
            if (data.authenticated) {
              // Redirect the user to the home page
              window.location.replace("/"); // Redirect to the root URL (/)
            }
          })
          .catch(error => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = '';
          });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Cal")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}


const chatbox = new Chatbox();
chatbox.display();