from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'username'}))
    password = forms.CharField(label='Password:', max_length=30,\
                               widget=forms.PasswordInput(attrs={'name': 'password',\
                                                                 'type': 'password'}))

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='First Name:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'first_name'}))
    last_name = forms.CharField(label='Last Name:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'last_name'}))
    email = forms.CharField(label='Email:', max_length=75,\
                               widget=forms.TextInput(attrs={'name': 'email'}))
    username = forms.CharField(label='Username:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'username'}))
    password1 = forms.CharField(label='Password:', max_length=30,\
                               widget=forms.PasswordInput(attrs={'name': 'password',\
                                                                 'type': 'password'}))
    password2 = forms.CharField(label='Confirm Password:', max_length=30,\
                               widget=forms.PasswordInput(attrs={'name': 'password',\
                                                                 'type': 'password'}),\
                               help_text=_('Enter the same password as above, for verification'))
    role = forms.ChoiceField(label='Role:',\
            choices=(
                (1, _('Student')),
                (2, ('Teacher')),
                (3, ('Employer')),
            ))
