import json
from channels.generic import websocket
from asgiref.sync import async_to_sync


class ChatConsumer(websocket.WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']

        # if not self.user.is_anonymous:
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.user.is_anonymous)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        username = ''
        if self.user.is_anonymous:
            username = 'Anonymous'
        else:
            username = self.user.username

        message = username + ': ' + text_data_json['message']

        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group

    def chat_message(self, event):
        # message = self.user.username + ': ' + event['message']
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
