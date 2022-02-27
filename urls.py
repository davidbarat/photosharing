from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth.views import LogoutView
from .views import SignUpView, CustomLoginView
from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]