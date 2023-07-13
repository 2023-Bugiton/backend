from django.shortcuts import render, redirect, get_object_or_404

from musics.models import Music, Favorite

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
    if request.user.is_authenticated:
        for music in music_list:
            music.is_liked = music.favorite_set.filter(user=request.user).exists()

    context ={
            'music_list': music_list,
            'music_title_list' : music_title_list,
        }
    
    return render(request, 'musics/music-list.html', context)


def music_like_view(request, id):
    if request.user.is_authenticated:
        music = get_object_or_404(Music, id=id)
        user = request.user

    # 이미 좋아요를 눌렀는지 확인
        if Favorite.objects.filter(user=user, music=music).exists():
            # 이미 좋아요를 눌렀을 경우 처리
            favorite = Favorite.objects.get(user=user, music=music)
            favorite.delete()
            # 좋아요 개수를 1 증가시킴
            music.like -= 1
            music.save()

        else:
            # 중개 모델을 생성하고 저장
            like = Favorite(user=user, music=music)
            like.save()

            # 좋아요 개수를 1 증가시킴
            music.like += 1
            music.save()

        return redirect('musics:music-list')
        
    return redirect('accouts:login')

def music_season_view(request):
    music_title_list = Music.objects.all()[:4]
    season = int(request.GET.get('season'))
    # 해당 시즌에 대한 게시물을 가져옴
    music_list = Music.objects.filter(category=season)
    if request.user.is_authenticated:
        for music in music_list:
            music.is_liked = music.favorite_set.filter(user=request.user).exists()

    
    context = {
        'music_list': music_list,
        'music_title_list' : music_title_list,
    }

    return render(request, 'musics/music_season.html', context)