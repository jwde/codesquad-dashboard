from django.contrib.auth.forms import AuthenticationForm
from django import forms
from registration.forms import RegistrationFormUniqueEmail
from models import Project
from django.utils.translation import ugettext_lazy as _

import json


class LoginForm(AuthenticationForm):
    pass


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['image', 'title', 'description',
                  'languagesframeworks',
                  'role', 'link']
        widgets = {
            'link': forms.TextInput(),
        }


class RegisterForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(label='First Name:', max_length=30,
                                 widget=forms.TextInput(attrs={'name': 'first_name'}),
                                 required=False)
    last_name = forms.CharField(label='Last Name:', max_length=30,
                                widget=forms.TextInput(attrs={'name': 'last_name'}),
                                required=False)
    error_css_class = 'error_message'
    role = forms.ChoiceField(label='Role:',
                             choices=(
                                 ('student', _('Student')),
                                 ('teacher', _('Teacher')),
                                 ('employer', _('Employer')),
                             ),
                             required=True)


class EditProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student')
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'] = forms.ImageField(label='Profile Picture:',
                                                widget=forms.FileInput(attrs={'name': 'profile_image'}),
                                                required=False)
        self.fields['about_me'] = forms.CharField(label='About Me:', max_length=1000,
                                                  widget=forms.Textarea(attrs={'name': 'about_me'}),
                                                  initial=student.about_me,
                                                  required=False)
        self.fields['languages'] = forms.CharField(label='Languages', max_length=200,
                                                   widget=forms.Textarea(attrs={'name': 'languages'}),
                                                   initial='\n'.join(student.languages),
                                                   required=False)

# class DynamicForm(forms.Form):
#     def set_fields(self, fields):
#         def question_to_field(question, name):
#             label = question.question_text
#             range_min_default = 1
#             range_max_default = 10
#             range_min = question.additional_info['range_min']\
#                         if 'range_min' in question.additional_info\
#                         else range_min_default
#             range_max = question.additional_info['range_max']\
#                         if 'range_max' in question.additional_info\
#                         else range_max_default
#             choices = ((c, _(c)) for c in question.additional_info['choices'])\
#                       if 'choices' in question.additional_info\
#                       else None
#             return {\
#                 'LF': lambda: forms.CharField(label=label, max_length=5000,\
#                                       widget=forms.Textarea(attrs={'name': name}),\
#                                       required=True),\
#                 'SF': lambda: forms.CharField(label=label, max_length=500,\
#                                       widget=forms.TextInput(attrs={'name': name}),\
#                                       required=True),\
#                 'MC': lambda: forms.ChoiceField(label=label,\
#                                         choices=choices,\
#                                         required=True),\
#                 'SS': lambda: forms.IntegerField(label=label,\
#                                          widget=forms.NumberInput(attrs=\
#                                              {'name': name,\
#                                               'type': 'range',\
#                                               'step': '1',\
#                                               'min': str(range_min),\
#                                               'max': str(range_max)}),\
#                                          required=True),\
#                 'SM': lambda: forms.MultipleChoiceField(label=label,\
#                                         choices=choices,\
#                                         widget=forms.CheckboxSelectMultiple(attrs={'name': name}),\
#                                         required=True)
#             }.get(question.question_type, lambda: None)()
#         for name,question in fields:
#             field = question_to_field(question, name)
#             if field:
#                 self.fields[name] = field
#
#     def __init__(self, *args, **kwargs):
#         fields = (('c{}'.format(n),v) for n,v in kwargs.pop('fields'))
#         super(DynamicForm, self).__init__(*args, **kwargs)
#         self.set_fields(fields)
#
#     def custom_responses(self):
#         for name,value in self.cleaned_data.items():
#             yield(name[1:], value)
