from django.contrib import admin
from .models import Music

# Register your models here.
@admin.register(Music)
class MusicModelAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'image','singer','category','like', 'created_at')
    list_filter = ('like',)
    search_fields = ('id',)
    search_help_text = '게시판 번호, 작성자 검색이 가능합니다.'

    actions = ['make_published']
