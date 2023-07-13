from django.urls import path

from chats.views import create_chatroom, chatroom_list, chatroom_detail, send_message

app_name = 'chats'

urlpatterns = [
    path('', chatroom_list, name='chatroom-list'),
    path('create/', create_chatroom, name='create-chatroom'),
    path('<int:id>/', chatroom_detail, name='chatroom-detail'),
    path('<int:room_id>/send-message/', send_message, name='send-message'),
]