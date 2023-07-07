from django import forms
from django.contrib.auth import get_user_model

class SignUpForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'my-class', 'placeholder': '아이디를 입력해주세요'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'my-class', 'placeholder': '비밀번호를 입력해주세요'}))
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter description here'}),
        }