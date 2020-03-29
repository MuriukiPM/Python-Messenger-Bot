import json
import six
from . import Bot

class Element(dict):
    __acceptable_keys = ['title', 'item_url', 'image_url', 'subtitle', 'buttons', 'default_action']
    def __init__(self, *args, **kwargs):
        kwargs = {k:v for k, v in kwargs.items() if k in self.__acceptable_keys}
        super(Element, self).__init__(*args, **kwargs)

    def to_json(self):
        return json.dumps({k:v for k, v in self.items() if k in self.__acceptable_keys})

class Button(dict):
    __acceptable_keys = ['title', 'type', 'url', 'payload', 'webview_height_ratio','messenger_extensions','fallback_url']
    def __init__(self, *args, **kwargs):
        kwargs = {k:v for k, v in kwargs.items() if k in self.__acceptable_keys}
        super(Button, self).__init__(*args, **kwargs)

    def to_json(self):
        return json.dumps({k:v for k, v in self.items() if k in self.__acceptable_keys})
    pass