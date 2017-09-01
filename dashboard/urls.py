from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^edit_project/(?P<pk>[0-9]+)/$', views.ProjectUpdateView.as_view(), name='edit_project'),
    # url(r'^my_forms/$', views.my_forms, name='my_forms'),
    # url(r'^form_responses/([0-9]+)/$', views.form_responses, name='form_responses'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^change_password/$', views.change_password, name='change_password'),
#     url(r'^create_form$', views.create_form, name='create_form'),
#     url(r'^form/([0-9]+)/$', views.form, name='form'),
#     url(r'^question/short_answer', views.template_short_answer, name=''),
#     url(r'^question/long_answer', views.template_long_answer, name=''),
#     url(r'^question/multiple_choice', views.template_multiple_choice, name=''),
#     url(r'^question/multiple_select', views.template_multiple_choice, name=''),
#     url(r'^question/slider', views.template_slider, name=''),
#     url(r'^question/invalid_form', views.template_invalid_form, name='')
]
