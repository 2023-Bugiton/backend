from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

def get_upload_path(instance, filename):
    # 이미지 파일이 저장될 경로를 설정하는 함수
    return f'{filename}'

class Perfume(models.Model):
    name = models.CharField(max_length=100,verbose_name='이름')
    description = models.TextField(verbose_name='내용')
    image = models.ImageField(verbose_name='이미지',null=True, blank=True,upload_to=get_upload_path)
    category = models.IntegerField(verbose_name='계절',blank=True, null=True)
    like = models.IntegerField(verbose_name='좋아요', default=0)
    user= models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=False)
    class Meta:
        db_table = 'perfume'

    def __str__(self):
        return self.name