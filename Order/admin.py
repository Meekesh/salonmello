from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["uuid","user","appointment_start_time","appointment_end_time"]
