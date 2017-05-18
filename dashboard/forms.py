from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.postgres.fields import JSONField, ArrayField
from django.utils.translation import ugettext, ugettext_lazy as _

import json

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
                               error_messages={'required': 'Enter the same password as above, for verification'},\
                               required=True)
    error_css_class='error_message'
    role = forms.ChoiceField(label='Role:',\
            choices=(
                ('student', _('Student')),
                ('teacher', _('Teacher')),
                ('employer', _('Employer')),
            ),\
            required=True)

class EditProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student')
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['about_me'] = forms.CharField(label='About Me:', max_length=1000,\
                                        widget=forms.TextArea(attrs={'name': 'about_me'}),\
                                        initial=student.about_me,\
                                        required=False)
        self.fields['languages'] = forms.CharField(label='Languages', max_length=200,\
                                         widget=forms.TextArea(attrs={'name': 'languages'}),\
                                         initial= ', '.join(student.languages),\
                                         required=False)
                                          #label='Languages:', max_length=200
                                          #widget=forms.TextInput(attrs={'name': 'languages'}),\
                                          #initial=student.languages,\
                                          #required=False)
        #changed here
        # self.fields['languages'] = ArrayField(forms.CharField(label='Languages:', max_length=200,\
        #                                 widget=forms.TextInput(attrs={'name': 'languages'}),\
        #                                 # initial=student.languages,\
        #                                 required=False))
#        self.fields['projects'] = forms.CharField(label='Projects:', max_length=1000,\
#                                        widget=forms.TextInput(attrs={'name': 'projects'}),\
#                                        initial=student.projects,\
#                                        required=False)
        self.fields['image'] = forms.ImageField(label='Profile Picture:',
                                                widget=forms.FileInput(attrs={'name': 'profile_image'}),
                                                required=False)


class EditProjectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student')
        super(EditProjectForm, self).__init__(*args, **kwargs)
        self.fields['project_title'] = forms.CharField(label='Project Title', max_length=100,\
                                             widget=forms.TextInput(attrs={'name': 'project_title'}),\
                                             required=True)
        self.fields['project_description'] = forms.CharField(label='Project Descrition', max_length=500,\
                                            widget=forms.TextArea(attrs={'name' : 'project_description'}),\
                                            required=True)
        self.fields['project_role'] = forms.CharField(label='My Role', max_length=150,\
                                            widget=forms.TextInput(attrs={'name' : 'project_role'}),\
                                            required=True)
        self.fields['project_link'] = forms.URLField(label='Project URL', max_length=100,\
                                            widget=forms.URLInput(attrs={'name' : 'project_link'}),\
                                            required=False)
        self.fields['project_languagesframeworks'] = forms.CharField(label='Languages', max_length=200,\
                                                    required=True)

        self.fields['project_image'] = forms.ImageField(label='Project Image:', required=False)









class DynamicForm(forms.Form):
    def set_fields(self, fields):
        def question_to_field(question, name):
            label = question.question_text
            range_min_default = 1
            range_max_default = 10
            range_min = question.additional_info['range_min']\
                        if 'range_min' in question.additional_info\
                        else range_min_default
            range_max = question.additional_info['range_max']\
                        if 'range_max' in question.additional_info\
                        else range_max_default
            choices = ((c, _(c)) for c in question.additional_info['choices'])\
                      if 'choices' in question.additional_info\
                      else None
            return {\
                'LF': lambda: forms.CharField(label=label, max_length=5000,\
                                      widget=forms.Textarea(attrs={'name': name}),\
                                      required=True),\
                'SF': lambda: forms.CharField(label=label, max_length=500,\
                                      widget=forms.TextInput(attrs={'name': name}),\
                                      required=True),\
                'MC': lambda: forms.ChoiceField(label=label,\
                                        choices=choices,\
                                        required=True),\
                'SS': lambda: forms.IntegerField(label=label,\
                                         widget=forms.NumberInput(attrs=\
                                             {'name': name,\
                                              'type': 'range',\
                                              'step': '1',\
                                              'min': str(range_min),\
                                              'max': str(range_max)}),\
                                         required=True),\
                'SM': lambda: forms.MultipleChoiceField(label=label,\
                                        choices=choices,\
                                        widget=forms.CheckboxSelectMultiple(attrs={'name': name}),\
                                        required=True)
            }.get(question.question_type, lambda: None)()
        for name,question in fields:
            field = question_to_field(question, name)
            if field:
                self.fields[name] = field

    def __init__(self, *args, **kwargs):
        fields = (('c{}'.format(n),v) for n,v in kwargs.pop('fields'))
        super(DynamicForm, self).__init__(*args, **kwargs)
        self.set_fields(fields)

    def custom_responses(self):
        for name,value in self.cleaned_data.items():
            yield(name[1:], value)
