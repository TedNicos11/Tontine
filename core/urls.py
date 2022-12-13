from django.urls import path
from .views import *

#  Create your urls here

urlpatterns = [
    path('<str:pk>/<str:user>', HomeView.as_view(), name="home"),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', ContactView.as_view(), name='contact'),
]