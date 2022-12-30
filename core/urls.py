from django.urls import path
from .views import *

#  Create your urls here

app_name = 'core'

urlpatterns = [
    path("", WelcomeView.as_view(), name="index"),
    path('<str:pk>/<str:user>/', HomeView.as_view(), name="home"),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('app/<str:pk>/<str:user>/', AppView.as_view(), name='app'),
]