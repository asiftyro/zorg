"""account/urls.py"""

from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("", views.AccountListView.as_view(), name="list"),
    path("<int:pk>/", views.AccountDetailView.as_view(), name="detail"),
    path("create/", views.AccountCreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.AccountUpdateView.as_view(), name="update"),
    path("self-update/", views.AccountSelfUpdateView.as_view(), name="selfupdate"),
    path("login/", views.AccountLoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("captcha-challange/", views.captcha_challange, name="captcha_challange"),
]
