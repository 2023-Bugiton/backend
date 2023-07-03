from django import forms
from .models import Post

class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

class PostCreateForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        fields = ['image','description','title','date','category','like']