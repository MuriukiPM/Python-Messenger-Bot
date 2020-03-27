import random
import sys
from flask import Flask, request
from libs.pymessenger_modified import Bot
from libs.pymessenger_modified import Element, Button
import logging as log
from os import environ as env
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
if 'ACCESS_TOKEN' not in env or 'VERIFY_TOKEN' not in env: 
    log.error('Be sure to set all environment vars')
    sys.exit(1)
ACCESS_TOKEN = env.get('ACCESS_TOKEN')
VERIFY_TOKEN = env.get('VERIFY_TOKEN')
bot = Bot(ACCESS_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Before allowing people to message your bot, Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook. 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not GET, it must be POST and we can just proceed with sending a message # back to user
    else:
    # get whatever message a user sent the bot
        output = request.get_json()
        # log.warn("OUTPUT: "+str(output))
        # print("output: "+str(output))
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message.get('message'):
                    if message['message'].get('text'):
                        response = get_generic()
                        bot.send_action(recipient_id, "mark_seen")
                        bot.send_action(recipient_id, "typing_on")
                        bot.send_generic_message(recipient_id, response)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        text, buttons = get_buttons()
                        bot.send_action(recipient_id, "mark_seen")
                        bot.send_action(recipient_id, "typing_on")
                        bot.send_button_message(recipient_id, text, buttons)
                if message.get('postback'):
                    bot.send_action(recipient_id, "mark_seen")
                    # bot.send_action(recipient_id, "typing_on")
                    bot.send_text_message(recipient_id, message['postback']['payload'])
        return "Message Processed"

#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're grateful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

def get_generic():
    elements = []
    default_action = Button(
        type="web_url",
        url="http://www.example.com/",
        webview_height_ratio="compact"
    )
    # log.warn("Buttons 1: "+str(buttons))
    elements.append(Element(
        title="Welcome!",
        image_url="https://images.pexels.com/photos/157675/fashion-men-s-individuality-black-and-white-157675.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        subtitle="We have the right stuff for everyone.",
        default_action=default_action,
        buttons=[Button(type="web_url",
                        url="http://www.example.com/",
                        title="View Website"
                        ),
                Button(type="postback",
                        title="Add to order",
                        payload="Got some payload!" 
                        )
                ]
        )
    )
    default_action = Button(
        type="web_url",
        url="http://www.example.com/",
        webview_height_ratio="compact"
    )
    elements.append(Element(
        title="Welcome!",
        image_url="https://images.pexels.com/photos/291762/pexels-photo-291762.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
        subtitle="We have the right stuff for you.",
        default_action=default_action,
        buttons=[Button(type="web_url",
                        url="http://www.example.com/",
                        title="Like us"
                        ), 
                Button(type="postback",
                        title="Add to order",
                        payload="Got some payload!"
                        )
                ]
        )
    )

    return elements

def get_buttons():
    text = 'Select'
    buttons = []
    button = Button(title='Yes', type='postback', payload="Selected yes")
    buttons.append(button)
    button = Button(title='No', type='postback', payload='Selected no')
    buttons.append(button)
    
    return text, buttons

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

def send_generic(recipient_id, response):
    bot.send_generic_message(recipient_id, response)
    return 'success'

if __name__ == '__main__':
    app.run(host="localhost",port=8080,load_dotenv=True)