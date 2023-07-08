from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from perfumes.views import perfume_list_view


app_name='posts' #html 에서 url을 name으로 설정할때 필요 posts:post-create 등

urlpatterns=[
    path('', perfume_list_view, name='perfume-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

