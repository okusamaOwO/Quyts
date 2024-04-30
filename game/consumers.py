import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Room
from .models import Question
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_code"]
        self.room_group_name = f"chat_{self.room_name}"
        self.groups_user = self.scope["user"]
        self.score = 0
        print(self.groups_user.username)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        
        if self.groups_user.is_authenticated:
            await sync_to_async(Room.add_participant)(room_code=self.room_name, learner=self.groups_user)

        await self.accept()

        # Get number of participants in the room
        count = await sync_to_async(Room.get_number_participants)(room_code=self.room_name)

        # Send count to client
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": count, "count" : count}
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        
        if self.groups_user.is_authenticated:
            await sync_to_async(Room.remove_participant)(room_code=self.room_name, learner=self.groups_user)

        # Get number of participants in the room
        count = await sync_to_async(Room.get_number_participants)(room_code=self.room_name)

        # Send count to client
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": count, "count" : count}
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        # Send message to room group

        count = await sync_to_async(Room.get_number_participants)(room_code=self.room_name)
      
        for x, y in text_data_json.items():
                question = await sync_to_async(Question.objects.get)(id=x)
                self.score +=1

        await self.send(text_data=json.dumps({'score':self.score}))
        # Send count to client
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": count, "count" : count}
        )

    async def chat_message(self, event):
        message = event["message"]
        count = event["count"]

        # Send message to client
        await self.send(text_data=json.dumps({"message": message, "count" : count}))
