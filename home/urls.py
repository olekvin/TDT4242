from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.home, name="home"),
    path("contact-us/", TemplateView.as_view(template_name="contact-us.html"), name="contact-us"),
]
