from django.urls import path
from .views import demo_view

urlpatterns = [
    path("", demo_view, name="demo"),
]
