from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Post(models.Model):
    image = models.ImageField(verbose_name='이미지',null=True, blank=True)
    description = models.TextField(verbose_name='내용',null=True)
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    date = models.IntegerField(verbose_name='여행일',blank=True,null=True)
    title = models.TextField(verbose_name='제목')
    like = models.IntegerField(verbose_name='좋아요', default=0)
    category = models.IntegerField(verbose_name='계절',blank=True, null=True)
    user= models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=False)