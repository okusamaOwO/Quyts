# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Room
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_code"]
        self.room_group_name = f"chat_{self.room_name}"
        self.groups_user = self.scope.get('user')

        # Join room group
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        if self.groups_user.is_authenticated:
            Room.add_participant(room_code= self.room_name,learner= self.groups_user )


        self.accept()

        # Get number of participants in the room
        count = Room.get_number_participants(room_code=self.room_name)

        # Send count to client
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": count}
        )

    def disconnect(self, close_code):
        # Leave room group
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        if self.groups_user.is_authenticated:
            Room.remove_participant(room_code= self.room_name, learner= self.groups_user)
        # Get number of participants in the room
        count = Room.get_number_participants(room_code=self.room_name)

        # Send count to client
        # Send count to client
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": count}
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        count = Room.get_number_participants(room_code=self.room_name)
        # Send count to client
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": count}
        )




    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
    
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
