from django import forms
from .models import Post

class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

class PostCreateForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        fields = ['location', 'cost', 'date', 'category', 'image','description','title']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 각 필드에 placeholder를 추가합니다.
        self.fields['title'].widget.attrs['placeholder'] = '서랍장 이름'
        self.fields['location'].widget.attrs['placeholder'] = '여행 위치를 작성해주세요'
        self.fields['cost'].widget.attrs['placeholder'] = '여행 총 경비를 작성해주세요'
        self.fields['description'].widget.attrs['placeholder'] = '서랍장을 소개해주세요'