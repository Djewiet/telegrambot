# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from .views import ( respond_to_websockets, 
                     post_event_on_telegram, 
                     count_user_action )

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.user = self.scope['user']
        self.send(text_data=json.dumps({
            'message' :{'text': 'Hello, welcome to our bot!!!. Click on one button'},
            'datetime': timezone.now().isoformat()
        }))

    def disconnect(self, close_code):
        pass


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['text']

        self.action = message
        count_user_action(message, self.user.id)
        
        # message to send to the telegram bot 
        message_to_send_content = {
        'user': "{} {}".format(self.user.first_name, self.user.last_name),
        'text': text_data_json['text'],
        'type': 'text',
        'source': 'CANDIDATE'
        }
        post_event_on_telegram(message_to_send_content)
        
        # we get the response from user action
        response = respond_to_websockets(
        text_data_json
        )
        now = timezone.now()
        response['source'] = 'BOT'
        self.send(text_data=json.dumps({
            'message': response,
            'action':message,
            'user': self.user.username,
            'datetime': now.isoformat()
        }))

