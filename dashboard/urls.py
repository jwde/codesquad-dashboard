from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from dashboard.forms import LoginForm
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html',\
                                        'authentication_form': LoginForm},\
        name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'},\
        name='logout'),
    # url(r'^password_change/$', auth_views.password_change, name='password_change'),
    # url(r'^password_change/done/$$', auth_views.password_change_done, name='password_change_done'),
    # url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
    #         auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
