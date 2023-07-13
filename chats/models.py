from django.db import models
from django.contrib.auth import get_user_model
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

User = get_user_model()

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, verbose_name='채팅방 이름')
    participants = models.ManyToManyField(User, related_name='chatrooms')

    
class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
