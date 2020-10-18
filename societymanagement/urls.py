from django.conf.urls import include,url

from .views import dashboard
from django.urls import path


urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^dashboard/", dashboard, name="dashboard"),
    
]