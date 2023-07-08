from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'my-class', 'placeholder': '이메일을 입력해주세요'}))
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'비밀번호를 입력해주세요'}))