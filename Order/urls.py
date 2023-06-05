from django.urls import path
from .views import CreateAppointment


urlpatterns = [
    path("new/",CreateAppointment, name="create-new"),
]