from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_attrs = {
            'username': {'class': 'form-control form-control-lg', 'placeholder': 'Choose a username'},
            'email': {'class': 'form-control form-control-lg', 'placeholder': 'Enter your email'},
            'password1': {'class': 'form-control form-control-lg', 'placeholder': 'Create your password'},
            'password2': {'class': 'form-control form-control-lg', 'placeholder': 'Confirm your password'},
        }
        for name, attrs in field_attrs.items():
            self.fields[name].widget.attrs.update(attrs)
            self.fields[name].label_suffix = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with that email already exists.')
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Username or email',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Password',
        })
        self.fields['username'].label_suffix = ''
        self.fields['password'].label_suffix = ''

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password and '@' in username:
            try:
                user = User.objects.get(email__iexact=username)
                self.cleaned_data['username'] = user.get_username()
            except User.DoesNotExist:
                pass
        return super().clean()
