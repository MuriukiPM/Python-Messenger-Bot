from .pymessenger_modified import Bot, Element, Button
# import logging as log

class PostbackSwitcher(object):
    '''
    Depending on the postback payload, choose and action
    '''
    def payload_string_to_response(self, payload_string, recipient_id, bot, Users, user):
        """Dispatch method"""
        self.user = user
        self.Users = Users
        self.bot = bot
        self.recipient_id = recipient_id
        method_name = 'selected_' + str(payload_string)
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid payload string")
        # Call the method as we return it
        return method()
 
    def selected_start(self):
        '''
        If the postback message is 'start' start conversation and create user
        '''
        self.user, error = get_started(self.recipient_id, self.bot, self.Users)
        if error is not None: 
            text = "Oops, something went wrong. We are working on it. Come back later!"
            self.bot.send_text_message(self.recipient_id, text=text)
            # log.error("ERROR: "+str(error))

            return error
        text, buttons = get_started_buttons(self.user)
        self.bot.send_action(self.recipient_id, "mark_seen")
        self.bot.send_action(self.recipient_id, "typing_on")
        self.bot.send_button_message(self.recipient_id, text, buttons)

        return None
 
    def selected_boy(self):
        '''
        If the postback message is 'boy' choose action and persist conversation
        '''
        self.user = get_user(self.recipient_id, self.Users)
        if self.user is None: return "Current user not in memory"
        self.Users[self.recipient_id]['user_data']['gender'] = 'Male'
        self.bot.send_action(self.recipient_id, "mark_seen")
        text, buttons = get_age_buttons(self.user, "It's a boy!")
        self.bot.send_action(self.recipient_id, "typing_on")
        self.bot.send_button_message(self.recipient_id, text, buttons)
        # self.bot.send_text_message(self.recipient_id, "It's a boy!")
        
        return None
 
    def selected_girl(self):
        '''
        If the postback message is 'girl' choose action and persist conversation
        '''
        self.user = get_user(self.recipient_id, self.Users)
        if self.user is None: return "Current user not in memory"
        self.Users[self.recipient_id]['user_data']['gender'] = 'Female'
        self.bot.send_action(self.recipient_id, "mark_seen")
        text, buttons = get_age_buttons(self.user, "It's a girl!")
        self.bot.send_action(self.recipient_id, "typing_on")
        self.bot.send_button_message(self.recipient_id, text, buttons)
        # self.bot.send_text_message(self.recipient_id, "It's a girl!")
        
        return None

    def selected_young(self):
        '''
        If the postback message is 'young' choose action and persist conversation
        '''
        self.user = get_user(self.recipient_id, self.Users)
        if self.user is None: return "Current user not in memory"
        self.Users[self.recipient_id]['user_data']['age'] = 'Young'
        self.bot.send_action(self.recipient_id, "mark_seen")
        text, buttons = get_result_button(self.user)
        self.bot.send_action(self.recipient_id, "typing_on")
        self.bot.send_button_message(self.recipient_id, text, buttons)
        
        return None
    
    def selected_old(self):
        '''
        If the postback message is 'old' choose action and persist conversation
        '''
        self.user = get_user(self.recipient_id, self.Users)
        if self.user is None: return "Current user not in memory"
        self.Users[self.recipient_id]['user_data']['age'] = 'Old'
        self.bot.send_action(self.recipient_id, "mark_seen")
        text, buttons = get_result_button(self.user)
        self.bot.send_action(self.recipient_id, "typing_on")
        self.bot.send_button_message(self.recipient_id, text, buttons)
        
        return None

    def selected_finish(self):
        '''
        If the postback message is 'finish' choose action and persist conversation
        '''
        self.user = get_user(self.recipient_id, self.Users)
        if self.user is None: return "Current user not in memory"
        self.bot.send_action(self.recipient_id, "mark_seen")
        mapping = {"Young":"bratty little",
                   "Old":"wise old",
                   "Female":"lady",
                   "Male":"guy"}
        text = "You are a {0} {1}".format(mapping[self.Users[self.recipient_id]['user_data']['age']],
                                          mapping[self.Users[self.recipient_id]['user_data']['gender']])
        _ = self.Users.pop(self.recipient_id) #delete the saved user
        self.bot.send_text_message(self.recipient_id, text)
        
        return None

# getting started
# TODO: Check for user in DB
def get_started(recipient_id, bot: Bot, Users):
    '''
    Create new user record and append to Users
    '''
    user = {}
    usr = bot.get_user_info(recipient_id, ["first_name", "last_name"])
    # log.warn("USER: "+str(usr))
    if usr is not None:
        user['user_info'], user['user_data'] = usr, {}
        Users[recipient_id] = user

        return user, None
    else: return None, 'Could not fetch user'

def get_user(recipient_id, Users):
    '''
    Check if we have user in memory
    '''
    if Users.get(recipient_id): return Users[recipient_id]
   
    return None

def get_started_buttons(user):
    '''
    Create starting message and buttons
    '''
    text="Hi "+user['user_info']['first_name']+"! Welcome to Hello World."
    "\n"
    "\nThanks for getting in touch with us on Messenger.Please selext one"
    buttons = []
    button = Button(title='Boy', type='postback', payload="boy")
    buttons.append(button)
    button = Button(title='Girl', type='postback', payload='girl')
    buttons.append(button)
    
    return text, buttons

def get_age_buttons(user, text):
    '''
    Create age selection buttons
    '''
    text = text+"\nSelect your age please"
    buttons = []
    button = Button(title='Young', type='postback', payload="young")
    buttons.append(button)
    button = Button(title='Old', type='postback', payload='old')
    buttons.append(button)
    
    return text, buttons

def get_result_button(user):
    '''
    Create age selection buttons
    '''
    text = "Done?"
    buttons = []
    button = Button(title='Finish', type='postback', payload="finish")
    buttons.append(button)

    return text, buttons