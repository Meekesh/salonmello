from django.urls import path, include, re_path
# from django.conf.urls import re_path
from .views import SignupView,LoginView,Logout,Contact,UserAppointments,DeleteUser,ContactList,ContactDelete

urlpatterns = [
    path('signup/',SignupView, name='signup'),
    path('login/', LoginView, name="login"),
    path('logout/',Logout, name="logout"),
    path("contactus/",Contact,name="contactus"),
    path("all-appointments/", UserAppointments, name="user-appointments"),
    path("user/<int:id>/delete/", DeleteUser,name="user-delete"),
    path("contact/", ContactList,name="contactus-list"),
    path("contact/<int:id>/delete/", ContactDelete,name="contactus-delete"),
]