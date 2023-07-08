from django.contrib import admin
from .models import Perfume

# Register your models here.
@admin.register(Perfume)
class PerfumeModelAdmin(admin.ModelAdmin):
    list_display = ('id','image','description','name','category','like',)
    list_filter = ('like',)
    search_fields = ('id',)
    search_help_text = '게시판 번호, 작성자 검색이 가능합니다.'

    actions = ['make_published']
