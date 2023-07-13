from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatRoom, ChatMessage
from .forms import ChatRoomForm

def create_chatroom(request):
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chatroom = form.save()
            chatroom.participants.add(request.user)  # 현재 사용자를 채팅방 참가자로 추가
            return redirect('chatrooms:chatroom-list')
    else:
        form = ChatRoomForm()

    context = {'form': form}
    return render(request, 'chats/create_chatroom.html', context)

@login_required
def chatroom_list(request):
    chatrooms = ChatRoom.objects.all()
    context = {'chatrooms': chatrooms}
    return render(request, 'chats/chatroom_list.html', context)


def chatroom_detail(request, id):
    chatroom = get_object_or_404(ChatRoom, id=id)
    messages = chatroom.messages.all()
    context = {
        'chatroom': chatroom,
        'messages': messages,
        }
    return render(request, 'chats/chatroom_detail.html', context)

def send_message(request, room_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        room = get_object_or_404(ChatRoom, id=room_id)
        message = ChatMessage(room=room, sender=request.user, content=content)
        message.save()
        
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})