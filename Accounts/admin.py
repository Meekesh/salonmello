from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MyUser, ContactUs, About

# Register your models here.
@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", 'first_name','last_name',"email","service",'user_type',"is_delete"]
    list_filter = ["user_type"]


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ["id","logo","description"]