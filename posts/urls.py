from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import post_detail_view, post_list_view,post_create_form_view,post_delete_view, post_update_view, my_page_view, season_view, sort_view, post_music_like, post_mySave_view, post_save_view, mySave_season_view, myPage_season_view, myPage_sort_view

app_name='posts' #html 에서 url을 name으로 설정할때 필요 posts:post-create 등

urlpatterns=[
    path('', post_list_view, name='post-list'),
    path('<int:id>/', post_detail_view, name='post-detail'),
    path('new/', post_create_form_view, name='post-create'),
    path('edit/<int:id>', post_update_view, name='post-update'),
    path('delete/<int:id>', post_delete_view, name="post-delete"),
    path('myPage/<int:id>', my_page_view, name="myPage"),

    path('season/', season_view, name="post-season"),
    path('sort/', sort_view, name="post-sort"),
    path('<int:id>/likes/', post_music_like, name='music-like'),

    path('mySave/', post_mySave_view, name='post-locker'),
    path('mySave/<int:id>', post_save_view, name='post-save'),
    path('mySave/season/', mySave_season_view, name="mySave-season"),

    path('myPage/season/', myPage_season_view, name="myPage-season"),
    path('myPage/sort/', myPage_sort_view, name="myPage-sort"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

