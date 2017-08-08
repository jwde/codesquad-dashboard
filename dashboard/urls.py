from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from dashboard.forms import LoginForm, RegisterForm
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/dashboard')),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^edit_project/$', views.edit_project, name='edit_project'),
    # url(r'^my_forms/$', views.my_forms, name='my_forms'),
    # url(r'^form_responses/([0-9]+)/$', views.form_responses, name='form_responses'),
    url(r'^accounts/',
        include('registration.backends.simple.urls')),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^change_password/$', views.change_password, name='change_password'),
#    url(r'^password_change/done/$$', auth_views.password_change_done, name='password_change_done'),
#    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
#    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
#            auth_views.password_reset_confirm, name='password_reset_confirm'),
#    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
#     url(r'^create_form$', views.create_form, name='create_form'),
#     url(r'^form/([0-9]+)/$', views.form, name='form'),
#     url(r'^question/short_answer', views.template_short_answer, name=''),
#     url(r'^question/long_answer', views.template_long_answer, name=''),
#     url(r'^question/multiple_choice', views.template_multiple_choice, name=''),
#     url(r'^question/multiple_select', views.template_multiple_choice, name=''),
#     url(r'^question/slider', views.template_slider, name=''),
#     url(r'^question/invalid_form', views.template_invalid_form, name='')
]
