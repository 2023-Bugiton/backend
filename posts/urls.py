from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import post_detail_view, post_list_view,post_create_form_view,post_delete_view

app_name='posts' #html 에서 url을 name으로 설정할때 필요 posts:post-create 등

urlpatterns=[
    path('', post_list_view, name='post-list'),
    path('<int:id>/', post_detail_view, name='post-detail'),
    path('new/', post_create_form_view, name='post-create'),
    path('delete/<int:id>', post_delete_view, name="post-delete"),

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)