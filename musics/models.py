from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

def get_upload_path(instance, filename):
    # 이미지 파일이 저장될 경로를 설정하는 함수
    return f'{filename}'

class Music(models.Model):
    title = models.CharField(max_length=100,verbose_name='노래 제목')
    singer = models.CharField(max_length=50,verbose_name='가수')
    image = models.ImageField(verbose_name='이미지',null=True, blank=True,upload_to=get_upload_path)
    category = models.IntegerField(verbose_name='계절',blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    like = models.IntegerField(verbose_name='좋아요', default=0)
    # like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_musics')
    user= models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=False)
    class Meta:
        db_table = 'music'

    def __str__(self):
        return self.title
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'music')