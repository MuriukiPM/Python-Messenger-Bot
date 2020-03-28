import json
import os
import requests
import logging as log
from requests_toolbelt import MultipartEncoder

from .graph_api import FacebookGraphApi
from . import utils

class Bot(FacebookGraphApi):
    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.messanging_graph_url = '{0}/me/messages'.format(self.graph_url)

    def send_recipient(self, recipient_id, payload):
        payload['recipient'] = {
            'id': recipient_id
        }
        return self.send_raw(payload)

    def send_message(self, recipient_id, message):
        payload={
            'message': message
        }
        return self.send_recipient(recipient_id, payload)

    def send_attachment(self, recipient_id, attachment_type, attachment_path):
        """
        Send an attachment to the specified recipient using local path.
        
        Input:
            recipient_id: recipient id to send to
            attachment_type: type of attachment (image, video, audio, file)
            attachment_path: Path of attachment
        Output:
            Response from API as <dict>
        """
        payload = {
            'recipient': {
                {
                    'id': recipient_id
                }
            },
            'message': {
                {
                    'attachment': {
                        'type': attachment_type,
                        'payload': {}
                    }
                }
            },
            'filedata': (os.path.basename(attachment_path), open(attachment_path, 'rb'))
        }
        multipart_data = MultipartEncoder(payload)

        return self.send_media_raw(multipart_data)

    def send_attachment_url(self, recipient_id, attachment_type, attachment_url):
        """
        Send an attachment to the specified recipient using URL.
        
        Input:
            recipient_id: recipient id to send to
            attachment_type: type of attachment (image, video, audio, file)
            attachment_url: URL of attachment
        Output:
            Response from API as <dict>
        """
        message = {
            'attachment': {
                'type': attachment_type,
                'payload': {
                    'url': attachment_url
                }
            }
        }

        self.send_message(recipient_id, message)

    def send_text_message(self, recipient_id, text):
        '''
        Send text messages to the specified recipient.
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/text-message
        
        Input:
            recipient_id: recipient id to send to
            message: message to send
        Output:
            Response from API as <dict>
        '''
        message = {
            'text': text
        }

        return self.send_message(recipient_id, message)

    def send_generic_message(self, recipient_id, elements):
        '''Send generic messages to the specified recipient.
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template
        Input:
            recipient_id: recipient id to send to
            elements: generic message elements to send
        Output:
            Response from API as <dict>
        '''
        # payload = {
        #     'recipient': {
        #         'id': recipient_id
        #     },
        #     'message': {
        #         "attachment": {
        #             "type": "template",
        #             "payload": {
        #                 "template_type": "generic",
        #                 "elements": elements
        #             }
        #         }
        #     }
        # }
        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
        }
        return self.send_message(recipient_id, message)

    def send_button_message(self, recipient_id, text, buttons):
        '''
        Send text messages to the specified recipient.
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/button-template
        
        Input:
            recipient_id: recipient id to send to
            text: text of message to send
            buttons: buttons to send
        Output:
            Response from API as <dict>
        '''

        # payload = {
        #     'recipient': {
        #         'id': recipient_id
        #     },
        #     'message': {
        #         "attachment": {
        #             "type": "template",
        #             "payload": {
        #                 "template_type": "button",
        #                 "text": text,
        #                 "buttons": buttons
        #             }
        #         }
        #     }
        # }
        message = {
            "attachment": {
                "type": "template",
                "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": buttons
                }
            }
        }

        return self.send_message(recipient_id, message)

    def send_action(self, recipient_id, action):
        '''Send typing indicators or send read receipts to the specified recipient.
        Image must be PNG or JPEG.
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions

        Input:
            recipient_id: recipient id to send to
            action: action type (mark_seen, typing_on, typing_off)
        Output:
            Response from API as <dict>
        '''
        # payload = {
        #     'recipient': {
        #         'id': recipient_id
        #     },
        #     'sender_action': action
        # }
        payload = {
            'sender_action': action
        }

        return self.send_recipient(recipient_id, payload)
        
    def send_raw(self, payload):
        auth = self.auth_args
        # log.warn('AUTH'+str(auth))
        return requests.post(
            self.messanging_graph_url,
            params=auth,
            json=payload
        ).json()

    def send_media_raw(self, data):
        # request_endpoint = '{0}/me/messages'.format(self.graph_url)
        multipart_header = {
            'Content-Type': data.content_type
        }
        return requests.post(
            self.messanging_graph_url, 
            data=data, 
            headers=multipart_header,
            params=self.auth_args
            ).json()
    
    def send_image(self, recipient_id, image_path):
        '''Send an image to the specified recipient.
        Image must be PNG or JPEG or GIF (more might be supported).
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/image-attachment
        Input:
            recipient_id: recipient id to send to
            image_path: path to image to be sent
        Output:
            Response from API as <dict>
        '''
        # payload = {
        #     'recipient': json.dumps(
        #         {
        #             'id': recipient_id
        #         }
        #     ),
        #     'message': json.dumps(
        #         {
        #             'attachment': {
        #                 'type': 'image',
        #                 'payload': {}
        #             }
        #         }
        #     ),
        #     'filedata': (image_path, open(image_path, 'rb'))
        # }
        # multipart_data = MultipartEncoder(payload)

        # return self.send_media_raw(multipart_data)
        return self.send_attachment(recipient_id, "image", image_path)

    def send_image_url(self, recipient_id, image_url):
        '''Send an image to specified recipient using URL.
        Image must be PNG or JPEG or GIF (more might be supported).
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/image-attachment
        Input:
            recipient_id: recipient id to send to
            image_url: url of image to be sent
        Output:
            Response from API as <dict>
        '''
        # payload = {
        #     'recipient': json.dumps(
        #         {
        #             'id': recipient_id
        #         }
        #     ),
        #     'message': json.dumps(
        #         {
        #             'attachment': {
        #                 'type': 'image',
        #                 'payload': {
        #                     'url': image_url
        #                 }
        #             }
        #         }
        #     )
        # }

        # return self.send_raw(payload)
        return self.send_attachment_url(recipient_id, "image", image_url)

    def send_audio(self, recipient_id, audio_path):
        '''Send audio to the specified recipient.
        Audio must be MP3 or WAV
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/audio-attachment
        Input:
            recipient_id: recipient id to send to
            audio_path: path to audio to be sent
        Output:
            Response from API as <dict>
        '''
        # payload = {
        #     'recipient': json.dumps(
        #         {
        #             'id': recipient_id
        #         }
        #     ),
        #     'message': json.dumps(
        #         {
        #             'attachment': {
        #                 'type': 'audio',
        #                 'payload': {}
        #             }
        #         }
        #     ),
        #     'filedata': (audio_path, open(audio_path, 'rb'))
        # }
        # multipart_data = MultipartEncoder(payload)
    
        # return self.send_media_raw(multipart_data)
        return self.send_attachment(recipient_id, "audio", audio_path)

    def send_audio_url(self, recipient_id, audio_url):
        '''Send audio to specified recipient using URL.
        Audio must be MP3 or WAV
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/audio-attachment
        Input:
            recipient_id: recipient id to send to
            audio_url: url of audio to be sent
        Output:
            Response from API as <dict>
        '''
        # payload = {
        #     'recipient': json.dumps(
        #         {
        #             'id': recipient_id
        #         }
        #     ),
        #     'message': json.dumps(
        #         {
        #             'attachment': {
        #                 'type': 'audio',
        #                 'payload': {
        #                     'url': audio_url
        #                 }
        #             }
        #         }
        #     )
        # }
        # return self.send_raw(payload)

        return self.send_attachment_url(recipient_id, "audio", audio_url)

    def send_video(self, recipient_id, video_path):
        '''Send video to the specified recipient.
        Video should be MP4 or MOV, but supports more (https://www.facebook.com/help/218673814818907).
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/video-attachment
        Input:
            recipient_id: recipient id to send to
            video_path: path to video to be sent
        Output:
            Response from API as <dict>
        '''
        # payload = {
        #     'recipient': json.dumps(
        #         {
        #             'id': recipient_id
        #         }
        #     ),
        #     'message': json.dumps(
        #         {
        #             'attachment': {
        #                 'type': 'video',
        #                 'payload': {}
        #             }
        #         }
        #     ),
        #     'filedata': (video_path, open(video_path, 'rb'))
        # }
        # multipart_data = MultipartEncoder(payload)
        
        # return self.send_media_raw(multipart_data)
        return self.send_attachment(recipient_id, "video", video_path)
        
    def send_video_url(self, recipient_id, video_url):
        '''Send video to specified recipient using URL.
        Video should be MP4 or MOV, but supports more (https://www.facebook.com/help/218673814818907).
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/video-attachment 
        Input:
            recipient_id: recipient id to send to
            video_url: url of video to be sent
        Output:
            Response from API as <dict>
        '''
        # payload = {
        #     'recipient': json.dumps(
        #         {
        #             'id': recipient_id
        #         }
        #     ),
        #     'message': json.dumps(
        #         {
        #             'attachment': {
        #                 'type': 'audio',
        #                 'payload': {
        #                     'url': video_url
        #                 }
        #             }
        #         }
        #     )
        # }
        # return self.send_raw(payload)

        return self.send_attachment_url(recipient_id, "video", video_url)

    def send_file(self, recipient_id, file_path):
        '''Send file to the specified recipient.
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/file-attachment
        Input:
            recipient_id: recipient id to send to
            file_path: path to file to be sent
        Output:
            Response from API as <dict>
        '''
        # payload = {
        #     'recipient': json.dumps(
        #         {
        #             'id': recipient_id
        #         }
        #     ),
        #     'message': json.dumps(
        #         {
        #             'attachment': {
        #                 'type': 'file',
        #                 'payload': {}
        #             }
        #         }
        #     ),
        #     'filedata': (file_path, open(file_path, 'rb'))
        # }
        # multipart_data = MultipartEncoder(payload)

        # return self.send_media_raw(multipart_data)
        return self.send_attachment(recipient_id, "file", file_path)

    def send_file_url(self, recipient_id, file_url):
        '''Send file to the specified recipient.
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/file-attachment
        Input:
            recipient_id: recipient id to send to
            file_url: url of file to be sent
        Output:
            Response from API as <dict>
        '''
        # payload = {
        #     'recipient': json.dumps(
        #         {
        #             'id': recipient_id
        #         }
        #     ),
        #     'message': json.dumps(
        #         {
        #             'attachment': {
        #                 'type': 'file',
        #                 'payload': {
        #                     'url': file_url
        #                 }
        #             }
        #         }
        #     )
        # }

        # return self.send_raw(payload)
        return self.send_attachment_url(recipient_id, "file", file_url)
    
    def get_user_info(self, user_id, fields=None):
        '''
            Query user info from User Profile API
            https://developers.facebook.com/docs/messenger-platform/identity/user-profile
            available by default fields are: name, first_name, last_name, profile_pic
            
            Input:
                user_id: Users PSID
                fields: fields to query
            Output:
                Response from API as JSON string
        '''
        params = {}
        if fields is not None and isinstance(fields, (list, tuple)): params['fields'] = ",".join(fields)
        params.update(self.auth_args)
        request_endpoint = '{0}/{1}'.format(self.graph_url, user_id)
        response = requests.get(request_endpoint, params=params)
        if response.status_code == 200: return response.json()
        
        return None

    def set_get_started(self, gs_obj):
        """
        Set a get started button shown on welcome screen for first time users
        https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/get-started-button
        
        Input:
          gs_obj: Your formatted get_started object as described by the API docs
        Output:
          Response from API as <dict>
        """
        request_endpoint = '{0}/me/messenger_profile'.format(self.graph_url)
        return requests.post(
            request_endpoint,
            params = self.auth_args,
            json = gs_obj
        ).json()

    def set_persistent_menu(self, pm_obj):
        """Set a persistent_menu that stays same for every user. Before you can use this, make sure to have set a get started button.
        https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/persistent-menu
        Input:
          pm_obj: Your formatted persistent menu object as described by the API docs
        Output:
          Response from API as <dict>
        """
        request_endpoint = '{0}/me/messenger_profile'.format(self.graph_url)
        return requests.post(
            request_endpoint,
            params = self.auth_args,
            json = pm_obj
        ).json()

    def remove_get_started(self):
            """delete get started button.
            https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/#delete
            Output:
            Response from API as <dict>
            """
            delete_obj = {"fields": ["get_started"]}
            request_endpoint = '{0}/me/messenger_profile'.format(self.graph_url)
            return requests.delete(
                request_endpoint,
                params = self.auth_args,
                json = delete_obj
            ).json()

    def remove_persistent_menu(self):
            """delete persistent menu.
            https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/#delete
            Output:
            Response from API as <dict>
            """
            delete_obj = {"fields": ["persistent_menu"]}
            request_endpoint = '{0}/me/messenger_profile'.format(self.graph_url)
            return requests.delete(
                request_endpoint,
                params = self.auth_args,
                json = delete_obj
            ).json()
