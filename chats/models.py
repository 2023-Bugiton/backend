from django.db import models
from django.contrib.auth import get_user_model
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

User = get_user_model()

class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Room(BaseModel):
    class Meta:
        db_table = "room"


class RoomJoin(BaseModel):

    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="roomJoin", db_column="user_id")
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="roomJoin", db_column="room_id")

    class Meta:
        db_table = "roomJoin"

class Message(BaseModel):
    message = models.CharField(max_length=500)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="message", db_column="user_id")
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="message", db_column="room_id")

    class Meta:
        db_table = "message"

    def __str__(self):
        return self.user_id.email

    def last_30_messages(self, room_id):
        return Message.objects.filter(room_id=room_id).order_by('created_at')[:30]
    

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        room_id = int(self.room_name)
        messages = Message.last_30_messages(self, room_id=room_id)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        user_id = data['user_id']
        room_id = int(self.room_name)
        user_contact = User.objects.filter(id=user_id)[0]
        room_contact = Room.objects.filter(id=room_id)[0]
        message_creat = Message.objects.create(
            user_id=user_contact,
            room_id=room_contact,
            message=data['message']
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message_creat)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.user_id.username,
            'content': message.message,
            'timestamp': str(message.created_at)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    # websocket 연결
    def connect(self):
        # room_name 파라미터를 chat/routing.py URl 에서 얻고, 열러있는 websocket에 접속
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # 인용이나 이스케이프 없이 사용자 지정 방 이름에서 직접 채널 그룹 이름을 구성
        # 그룹 이름에는 문자, 숫자, 하이픈 및 마침표만 사용할 수 있어서 튜토리얼 예제 코드는 다른 문자가 있는 방이름 에서는 실패
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group / 그룹에 참여
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # websocket 연결을 수락 / connect() 메서드 내에서 accept()를 호출하지 않으면 연결이 거부되고 닫힌다.
        self.accept()

    # websocket 연결 해제
    def disconnect(self, close_code):
        # Leave room group / 그룹에서 탈퇴
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))