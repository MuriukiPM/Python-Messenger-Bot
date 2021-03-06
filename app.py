import sys
from flask import Flask, request
from libs.pymessenger_modified import Bot
from libs.pymessenger_modified import Element, Button
from libs.utils import PostbackSwitcher
import logging as log
from os import environ as env
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
secrets = ['PAGE_ACCESS_TOKEN','VERIFY_TOKEN','APP_SECRET']
if not all([secret in env for secret in secrets]): 
    log.error('Be sure to set all environment vars')
    sys.exit(1)
PAGE_ACCESS_TOKEN = env.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = env.get('VERIFY_TOKEN')
APP_SECRET = env.get('APP_SECRET')
API_VERSION = env.get('API_VERSION')
Users = {}
postbackSwitcher  = PostbackSwitcher()
bot = Bot(PAGE_ACCESS_TOKEN, api_version=API_VERSION, app_secret=APP_SECRET)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Before allowing people to message your bot, Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook. 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not GET, it must be POST and we can just proceed with sending a message back to user
    else:
    # get whatever message a user sent the bot
        output = request.get_json()
        # log.warn("OUTPUT: "+str(output))
        log.warn("USERS: "+str(Users))
        actions(output)
        return "Message Processed"

# TODO: Complete logic for when user record is not in memory
def actions(output):
    global Users
    for event in output['entry']:
        messaging = event['messaging']
        # log.warn("MESSAGING: "+str(messaging))
        for message in messaging:
            #Facebook Messenger ID for user so we know where to send response back to
            recipient_id = message['sender']['id']
            if message.get('postback'):
                error = postbackSwitcher.payload_string_to_response(payload_string=message['postback']['payload'],
                                                                    recipient_id = recipient_id,
                                                                    bot=bot,
                                                                    Users=Users,
                                                                    user=None
                                                                    )
                if error is not None: log.error("ERROR: "+str(error))
            # elif message.get('message'):
            #     user = get_user(recipient_id)
            #     if user is None: pass
            #     if message['message'].get('text'):
            #         response = get_generic()
            #         try:
            #             res = bot.send_action(recipient_id, "mark_seen")
            #             # log.warn('RESPONSE: '+str(res))
            #             if res.get('error'):
            #                 log.error('ERROR: '+str(res['error']))

            #                 continue
            #         except Exception as e:
            #             log.error('ERROR: '+str(e))

            #             continue
            #         try:
            #             res = bot.send_action(recipient_id, "typing_on")
            #             # log.warn('RESPONSE: '+str(res))
            #             if res.get('error'):
            #                 log.error('ERROR: '+str(res['error']))

            #                 continue
            #         except Exception as e:
            #             log.error('ERROR: '+str(e))

            #             continue
            #         try:
            #             res = bot.send_generic_message(recipient_id, response)
            #             # log.warn('RESPONSE: '+str(res))
            #             if res.get('error'):
            #                 log.error('ERROR: '+str(res['error']))

            #                 continue
            #         except Exception as e:
            #             log.error('ERROR: '+str(e))

            #             continue
            #     #if user sends us a GIF, photo,video, or any other non-text item
            #     elif message['message'].get('attachments'):
            #         text, buttons = get_buttons()
            #         bot.send_action(recipient_id, "mark_seen")
            #         bot.send_action(recipient_id, "typing_on")
            #         bot.send_button_message(recipient_id, text, buttons)

            #         continue

    return

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