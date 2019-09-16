from django.urls import path
from patterns import patterns

from . import views
from django.contrib.auth import views as auth_views
from .views import activate
from django.conf.urls import url
#from django.conf.urls import patterns

#from crossmedia.forms import RegisterFormStepOne, RegisterFormStepTwo
#from crossmedia.views import FormWizardView

urlpatterns = [
    path('', views.home, name='home'),
    #path('login_old/', views.login, name='login_old'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='crossmedia/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='crossmedia/logout.html'), name='logout'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('account_activation_email/', views.account_activation_email, name='account_activation_email'),
    path('register_step_one/', views.register_form_step_one, name='register_step_one'),
    path('register_step_two/', views.register_form_step_two, name='register_step_two'),
    path('register_step_three/', views.register_form_step_three, name='register_step_three'),
    path('friends/', views.friendlist, name='friendlist'),
    path(r'friends/<id>/', views.friend_profile, name='friend_profile'),
    path(r'post-create/', views.post_create, name='post_create'),
    path(r'post/<id>/edit/', views.post_update, name='update'),
    path('my_posts/', views.post_detail, name='my-posts'),
    path(r'post/<id>/delete/', views.post_delete, name='delete-post'),
    path(r'post/<id>/like/', views.post_like, name='like-post'),
    path('people/', views.people_you_may_know, name='people-you-may-know'),
    path(r'people/<id>/send-request/', views.send_request, name='send_request'),
    path('friend-requests/', views.friend_requests, name='friend-requests'),
    path(r'accept-request/<id>/', views.accept_friend_request, name='accept-request'),
    path('children-list/', views.children_list, name='children-list'),
]