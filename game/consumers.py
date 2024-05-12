import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Room
from .models import Question
class RoomConsumer(AsyncWebsocketConsumer):
    online_users = 0
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_code"]
        self.room_group_name = f"chat_{self.room_name}"
        self.groups_user = self.scope["user"]
        self.chat_text = ""
        self.score = 0
        print(self.groups_user.username)
        # Join room group
        RoomConsumer.online_users += 1
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        
        # if self.groups_user.is_authenticated:
        #     await sync_to_async(Room.add_participant)(room_code=self.room_name, learner=self.groups_user)

        await self.accept()

        # Get number of participants in the room
        #count = await sync_to_async(Room.get_number_participants)(room_code=self.room_name)

        # Send count to client
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "number_user_message",  "count" : RoomConsumer.online_users}
        )

    async def disconnect(self, close_code):
        # if self.groups_user.is_authenticated:
        #     await sync_to_async(Room.remove_participant)(room_code=self.room_name, learner=self.groups_user)
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

        if close_code != 1000:
            # Xử lý khi người dùng rời khỏi trang
            RoomConsumer.online_users -= 1
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "number_user_message",  "count" : RoomConsumer.online_users}
            )
            

        # count = await sync_to_async(Room.get_number_participants)(room_code=self.room_name)    
        # Get number of participants in the room

        # Send count to client


    async def receive(self, text_data):
        text_data_dict = json.loads(text_data)

        if text_data_dict["type"] == 'chat' :
            
        
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "user_name" : self.groups_user.username, "message": text_data_dict["text"]}
            )
            
            # count = await sync_to_async(Room.get_number_participants)(room_code=self.room_name)   
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "number_user_message",  "count" : RoomConsumer.online_users}
            )
        elif text_data_dict["type"] == 'start_game' : 
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "start_game_message", "run" : text_data_dict["run"]}
            )
        elif text_data_dict["type"] == 'leave_room' :
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "leave_room_message",}
            )
        elif text_data_dict["type"] == 'user_score':
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "user_score_message", 'score' : text_data_dict["user_scrore"] , 'user_name' : text_data_dict["user_name"]}
            )
            


        # count = await sync_to_async(Room.get_number_participants)(room_code=self.room_name)
      
        # for x, y in text_data_json.items():
        #         question = await sync_to_async(Question.objects.get)(id=x)
        #         self.score +=1

        # await self.send(text_data=json.dumps({'score':self.score}))
        # Send count to client
        # await self.channel_layer.group_send(
        #     self.room_group_name, {"type": "chat.message", "message": count, "count" : count}
        # )

    async def chat_message(self, event):
        type = event["type"]
        message = event["message"]
        user_name = event["user_name"]


        # Send message to client
        await self.send(text_data=json.dumps({"type" : type,"user_name" : user_name,"message": message}))
        
    async def number_user_message(self, event): 
        count = event["count"]
        type = event["type"]
        await self.send(text_data=json.dumps({"type" : type , "count" : count}))
    
    async def start_game_message(self, event): 
        run = event["run"]
        type = event["type"]
        await self.send(text_data=json.dumps({"type" : type , "run" : run}) )
    async def leave_room_message(self, event): 
        RoomConsumer.online_users -= 1
        await self.send(text_data=json.dumps({"type" : "number_user_message" , "count" : RoomConsumer.online_users}) )
        
    async def user_score_message(self, event): 
        score = event["score"]
        user_name = event["user_name"]
        await self.send(text_data=json.dumps({"type" : event["type"] , "score" :score, 'user_name' : user_name }) )