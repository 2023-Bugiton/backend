from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=64,verbose_name="사용자이름")
    password = models.CharField(max_length=64, verbose_name="비밀번호")
    email = models.EmailField(max_length=128, verbose_name="이메일")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        verbose_name ="사용자"
        verbose_name_plural = "사용자"