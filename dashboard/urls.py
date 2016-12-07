from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from dashboard.forms import LoginForm, RegisterForm
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/dashboard')),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/([a-z]+)$', views.dashboard),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^my_forms/$', views.my_forms, name='my_forms'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html',\
                                        'authentication_form': LoginForm},\
        name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
#    url(r'^password_change/$', auth_views.password_change, name='password_change'),
#    url(r'^password_change/done/$$', auth_views.password_change_done, name='password_change_done'),
#    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
#    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
#            auth_views.password_reset_confirm, name='password_reset_confirm'),
#    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^form/([0-9]+)/$', views.form, name='form'),
]
