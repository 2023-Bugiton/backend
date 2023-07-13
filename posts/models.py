from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

# Create your models here.

class Post(models.Model):
    location = models.CharField(max_length=100,verbose_name='여행위치', null=True)
    cost = models.IntegerField(verbose_name='여행경비', blank=True,null=True)
    image = models.ImageField(verbose_name='이미지',null=True, blank=True)
    description = models.TextField(verbose_name='내용',null=True)
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    date = models.IntegerField(verbose_name='여행일',blank=True,null=True)
    title = models.CharField(max_length=100, verbose_name='제목')
    where = models.IntegerField(verbose_name='국내 국외', null=True, default=0)
    category = models.IntegerField(verbose_name='계절',blank=True)
    start = models.CharField(max_length=100, verbose_name='여행시작날짜', null=True)
    end = models.CharField(max_length=100, verbose_name='여행끝날짜', null=True)
    user= models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=False)
    class Meta:
        db_table = 'post'

class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')