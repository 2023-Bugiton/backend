from django.shortcuts import render, redirect, get_object_or_404

from musics.models import Music

# Create your views here.
def music_list_view(request):

    music_title_list = Music.objects.all()[:4]
    #perfume_list = Perfume.objects.filter(user_id = request.user)
    
    if request.GET.get('order') == 'recent':        
        music_list = Music.objects.all().order_by('-created_at')

    elif request.GET.get('order') == 'popular':
        music_list = Music.objects.all().order_by('-like')
        
    else:
        music_list = Music.objects.all()

    context ={
            'music_list': music_list,
            'music_title_list' : music_title_list,
        }
    
    return render(request, 'musics/music-list.html', context)


def music_like_view(request, music_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Music, pk=music_pk)

        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
        return redirect('musics:music-list')
    return redirect('accouts:login')