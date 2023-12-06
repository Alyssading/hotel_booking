from django import forms
from django.forms import widgets, fields

from app.models import User


class RegisterForm(forms.ModelForm):
    """
    Registration form 
    """
    first_name = fields.CharField(
        label='first name',
        required=True,
        max_length=64,
        min_length=2,
        widget=widgets.TextInput(attrs={'class': 'form-control loon reg_email'})
    )
    last_name = fields.CharField(
        label='last name',
        required=True,
        max_length=64,
        min_length=2,
        widget=widgets.TextInput(attrs={'class': 'form-control loon reg_email'})
    )
    username = fields.CharField(
        label='username',
        required=True,
        max_length=64,
        min_length=3,
        widget=widgets.TextInput(attrs={'class': 'form-control loon reg_email'})
    )
    email = fields.EmailField(
        label='email',
        required=True,
        widget=widgets.TextInput(attrs={'class': 'form-control loon reg_email'})
    )
    password = fields.CharField(
        label='password',
        required=True,
        max_length=64,
        min_length=3,
        widget=widgets.PasswordInput(attrs={'class': 'form-control loon reg_pwd'})
    )
    re_password = fields.CharField(
        label='confirm password',
        required=True,
        max_length=64,
        min_length=3,
        widget=widgets.PasswordInput(attrs={'class': 'form-control loon reg_repwd'})
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            're_password',
        ]
class LoginForm(forms.Form):
    """
    login form
    """
    username = fields.CharField(
        label='username',
        required=True,
        max_length=64,
        min_length=3,
        widget=widgets.TextInput(attrs={'class': 'form-control loon luser'})
    )
    password = fields.CharField(
        label='password',
        required=True,
        max_length=64,
        min_length=3,
        widget=widgets.PasswordInput(attrs={'class': 'form-control loon lpass'})
    )


class UserInfoForm(forms.ModelForm):
    """Modify User Information Form"""
    username = fields.CharField(
        label='username',
        required=False,
        widget=widgets.TextInput(attrs={'class': 'form-control loon'})
    )
    email = fields.EmailField(
        label='email',
        required=False,
        widget=widgets.TextInput(attrs={'class': 'form-control loon'})
    )
    first_name = fields.CharField(
        label='first name',
        required=True,
        max_length=64,
        min_length=1,
        widget=widgets.TextInput(attrs={'class': 'form-control loon reg_email'})
    )
    last_name = fields.CharField(
        label='last name',
        required=True,
        max_length=64,
        min_length=1,
        widget=widgets.TextInput(attrs={'class': 'form-control loon reg_email'})
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class ChangePwdForm(forms.Form):
    """Change Password Form"""
    password = fields.CharField(
        label='password',
        required=True,
        max_length=64,
        min_length=3,
        widget=widgets.PasswordInput(attrs={'class': 'form-control loon reg_pwd'})
    )
    re_password = fields.CharField(
        label='confirm password',
        required=True,
        max_length=64,
        min_length=3,
        widget=widgets.PasswordInput(attrs={'class': 'form-control loon reg_repwd'})
    )

    new_password = fields.CharField(
        label='new password',
        required=True,
        max_length=64,
        min_length=3,
        widget=widgets.PasswordInput(attrs={'class': 'form-control loon reg_repwd'})
    )
