from .views import LoginUserView
from django.urls import path
from . import views

urlpatterns = [
    path("login/", LoginUserView.as_view()),
    path("accounts/", views.UserView.as_view()),
    path("accounts/newest/<int:num>/", views.UserDetailView.as_view()),
    path("accounts/<pk>/", views.UpdateUserView.as_view()),
    path("accounts/<pk>/management/", views.ActivateOrDeactivateAccountView.as_view()),
]