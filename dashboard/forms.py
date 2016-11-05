from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'username'}))
    password = forms.CharField(label='Password:', max_length=30,\
                               widget=forms.PasswordInput(attrs={'name': 'password',\
                                                                 'type': 'password'}))

class LoginForm(AuthenticationForm):
	first_name = forms.CharField(label='First Name:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'first_name'}))
    last_name = forms.CharField(label='Last Name:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'last_name'}))
    email = forms.CharField(label='Email:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'email'}))
    username = forms.CharField(label='Username:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'username'}))
    password = forms.CharField(label='Password:', max_length=30,\
                               widget=forms.PasswordInput(attrs={'name': 'password',\
                                                                 'type': 'password'}))
    role = forms.CharField(label='Role:', max_length=30,\
                               widget=forms.TextInput(attrs={'name': 'username'}))
    role = forms.ChoiceField(label='Role:', max_length=30,\
    						   choices=['Student', 'Teacher', 'Employer'])