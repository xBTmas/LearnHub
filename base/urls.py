from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginPage, name="Login"),
    path("logout/", views.LogoutPage, name="Logout"),
    path("register/", views.RegisterPage, name="Register"),
    path("", views.Home, name="Home"),
    path("profile/<str:no>", views.userProfile, name="profile"),
    path("room/<str:no>/", views.room, name="room"),
    path("create-room/", views.createRoom, name="createRoom"),
    path("update-room/<str:no>/", views.updateRoom, name="updateRoom"),
    path("delete-room/<str:no>/", views.deleteRoom, name="deleteRoom"),
    path("delete-message/<str:no>/", views.deleteMessage, name="deleteMessage"),
    path("updateUser/", views.updateUser, name="updateUser"),
    path("topicsPage/", views.topicsPage, name="topicsPage"),
]
