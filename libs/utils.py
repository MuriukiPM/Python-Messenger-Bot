class PostbackSwitcher(object):
    def payload_string_to_response(self, payload_string, user):
        """Dispatch method"""
        self.user = user
        method_name = 'selected_' + str(payload_string)
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid payload string")
        # Call the method as we return it
        return method()
 
    def selected_boy(self):
        return None
 
    def selected_girl(self):
        return None
 
    def selected_start(self):
        return None