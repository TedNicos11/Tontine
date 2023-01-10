from django.urls import path
from .views import *

#  Create your urls here

app_name = 'core'

urlpatterns = [
    path('', WelcomeView.as_view(), name="index"),
    path('<str:pk>/<str:user>/', HomeView.as_view(), name="home"),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('app/<str:pk>/<str:user>/', AppView.as_view(), name='app'),
    path("app/<str:pk>/<str:user>/new-tontine/", CreateTontine.as_view(), name="new_tontine"),
    path("app/<str:pk>/<str:user>/my-tontines/", ListTontine.as_view(), name="all_tontines"),
<<<<<<< HEAD
    path("app/details/<str:tont_id>/<slug:tontine>/", DetailTontine.as_view(), name="detail_tontine"),
=======
    path("app/<str:pk>/<str:user>/<str:tont_id>/<slug:tontine>/", DetailTontine.as_view(), name="detail_tontine"),
>>>>>>> 073e4ed2bb2b35730268356e537717c34398ef09
    path("app/<str:pk>/<str:user>/<str:tont_id>/<str:tontine>/update", UpdateTontine.as_view(), name="update_tontine"),
    path("app/<str:pk>/<str:user>/<str:tont_id>/<str:tontine>/delete", DeleteTontine.as_view(), name="delete_tontine"),
    path("app/<str:pk>/<str:user>/join", JoinTontine.as_view(), name="join_tontine"),
]