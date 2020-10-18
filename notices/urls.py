from django.urls import path
from . import views

urlpatterns = [
    path("", views.notice_index, name="notice_index"),
    path("<int:pk>/", views.notice_detail, name="notice_detail"),
]