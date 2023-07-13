from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from musics.views import music_list_view, music_like_view, music_season_view

app_name='music' #html 에서 url을 name으로 설정할때 필요 posts:post-create 등

urlpatterns=[
    path('', music_list_view, name='music-list'),
    path('<int:id>/likes/', music_like_view, name='music-like'),
    path('season/', music_season_view, name='music-season'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

