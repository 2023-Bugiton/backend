from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

class UserBaseForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'

class SignUpForm(UserBaseForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력해주세요'}))
    email = forms.CharField(label='', widget=forms.EmailInput(attrs={'placeholder': '이메일을 입력해주세요'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 재입력해주세요'}))
    class Meta(UserBaseForm.Meta):
        fields = ['username', 'email', 'password', 'password2']

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'비밀번호를 입력해주세요'}))