from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'my-class', 'placeholder': '이메일을 입력해주세요'}))
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'last_name', 'first_name', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 각 필드에 placeholder를 추가합니다.
        self.fields['username'].widget.attrs['placeholder'] = '아이디를 입력해주세요'
        self.fields['first_name'].widget.attrs['placeholder'] = '이름을 입력해주세요'
        self.fields['last_name'].widget.attrs['placeholder'] = '성을 입력해주세요'
        self.fields['password1'].widget.attrs['placeholder'] = '비밀번호를 입력해주세요'
        self.fields['password2'].widget.attrs['placeholder'] = '비밀번호를 확인해주세요'

        # 각 필드의 label과 help_text를 비우기
        self.fields['username'].label = ''
        self.fields['username'].help_text = None
        self.fields['first_name'].label = ''
        self.fields['first_name'].help_text = None
        self.fields['last_name'].label = ''
        self.fields['last_name'].help_text = None
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = None
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = None


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'비밀번호를 입력해주세요'}))