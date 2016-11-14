from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

class LoginForm(AuthenticationForm):
    pass

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='First Name:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'first_name'}),\
                               required=False)
    last_name = forms.CharField(label='Last Name:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'last_name'}),\
                               required=False)
    email = forms.EmailField(label='Email:', required=True)
    username = forms.CharField(label='Username:', max_length=150,\
                               widget=forms.TextInput(attrs={'name': 'username'}),\
                               required=True)
    password1 = forms.CharField(label='Password:',\
                               widget=forms.PasswordInput(attrs={'name': 'password1',\
                                                                 'type': 'password'}),\
                               required=True)
    password2 = forms.CharField(label='Confirm Password:',\
                               widget=forms.PasswordInput(attrs={'name': 'password2',\
                                                                 'type': 'password'}),\
                               help_text=_('Enter the same password as above, for verification'),\
                               required=True)
    role = forms.ChoiceField(label='Role:',\
            choices=(
                ('student', _('Student')),
                ('teacher', _('Teacher')),
                ('employer', _('Employer')),
            ),\
            required=True)
