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
    # like = models.IntegerField(verbose_name='좋아요', default=0)
    where = models.IntegerField(verbose_name='국내 국외', null=True, default=0)
    category = models.IntegerField(verbose_name='계절',blank=True)
    user= models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=False)
    class Meta:
        db_table = 'post'

