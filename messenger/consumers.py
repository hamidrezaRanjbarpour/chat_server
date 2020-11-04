import json
from channels.generic import websocket
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from .models import Message
from django.shortcuts import Http404


class ChatConsumer(websocket.WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.get_most_recent_messages(room_name=self.room_name)
        content = {
            'command': 'fetch_messages',
            'messages': self.messages_to_json(messages)
        }

        self.send_chat_message(content)

    def create_new_message(self, data):
        print('new messages')
        author = data['from']
        print(author)
        try:
            user = User.objects.get(username=author)
        except User.DoesNotExist:
            raise Http404("User with this username doesn't exist.")

        new_message = Message.objects.create(author=user, content=data['message'], room_name=self.room_name)
        content = {
            'command': 'new_message',
            'message': self.current_message_to_json(new_message)
        }

        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': create_new_message,

    }

    def messages_to_json(self, messages):
        result = []
        for m in messages:
            result.append(self.current_message_to_json(m))

        return result

    def current_message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'time_stamp': str(message.time_stamp)
        }

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
        data = json.loads(text_data)
        print(data)
        # username = ''
        # if self.user.is_anonymous:
        #     username = 'Anonymous'
        # else:
        #     username = self.user.username
        #
        # message = username + ': ' + text_data_json['message']

        # fetch_messages(text_data_json) or new_message(text_data_json)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': message,
            }
        )

    # Receive message from room group

    def chat_message(self, event):
        # message = self.user.username + ': ' + event['message']
        content = event['content']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'content': content
        }))
