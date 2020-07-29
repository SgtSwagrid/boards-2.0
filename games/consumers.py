import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

class BoardUpdateConsumer(WebsocketConsumer):

    def connect(self):

        self.board_code = self.scope['url_route']['kwargs']['board_code']
        self.group_name = 'board_' + self.board_code

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name)

    def update_board(self, event):

        self.send(text_data=json.dumps({}))

def notify_board(board):

    async_to_sync(get_channel_layer().group_send)(
        'board_' + board.code, {'type': 'update_board'})

class MessageConsumer(WebsocketConsumer):

    def connect(self):

        self.board_code = self.scope['url_route']['kwargs']['board_code']
        self.group_name = 'messages_' + self.board_code

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name)

    def receive(self, text_data):

        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
                'type': 'send_message',
                'message': json.loads(text_data)['message']
            })

    def send_message(self, event):

        self.send(text_data=json.dumps({
            'message': event['message']}))