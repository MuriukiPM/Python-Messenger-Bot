import json
import six

from . import Bot

# update: 03-26-20 - updated package to include 'default_action'
# update: 03-27-20 - remove check for py2
# update: 03-27-20 - move from init to models
class Element(dict):
    __acceptable_keys = ['title', 'item_url', 'image_url', 'subtitle', 'buttons', 'default_action']
    def __init__(self, *args, **kwargs):
        # if six.PY2:
        #     kwargs = {k:v for k, v in kwargs.iteritems() if k in self.__acceptable_keys}
        # else:
        kwargs = {k:v for k, v in kwargs.items() if k in self.__acceptable_keys}
        super(Element, self).__init__(*args, **kwargs)

    def to_json(self):
        # return json.dumps({k:v for k, v in self.iteritems() if k in self.__acceptable_keys})
        return json.dumps({k:v for k, v in self.items() if k in self.__acceptable_keys})

# update: 03-26-20 - updated package to implement Button
# update: 03-27-20 - remove check for py2
class Button(dict):
    __acceptable_keys = ['title', 'type', 'url', 'payload', 'webview_height_ratio','messenger_extensions','fallback_url']
    def __init__(self, *args, **kwargs):
        # if six.PY2:
        #     kwargs = {k:v for k, v in kwargs.iteritems() if k in self.__acceptable_keys}
        # else:
        kwargs = {k:v for k, v in kwargs.items() if k in self.__acceptable_keys}
        super(Button, self).__init__(*args, **kwargs)

    def to_json(self):
        # return json.dumps({k:v for k, v in self.iteritems() if k in self.__acceptable_keys})
        return json.dumps({k:v for k, v in self.items() if k in self.__acceptable_keys})
    pass