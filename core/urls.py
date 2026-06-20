from django.urls import path

from core.apps import CoreConfig

from .views import AboutUsView, HomePageView

app_name = CoreConfig.name

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about_us", AboutUsView.as_view(), name="about_us"),
]
