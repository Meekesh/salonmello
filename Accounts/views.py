from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.backends import ModelBackend

from Common.models import ConfigChoice
from Order.models import Order
from .models import ContactUs

User = get_user_model()
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate


# Create your views here.
@csrf_exempt
def SignupView(request):
    user_type = ConfigChoice.objects.filter(category__name="User Type").exclude(name="Super User")
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        year = request.POST.get("year")
        month = request.POST.get("month")
        day = request.POST.get("date")
        password1 = request.POST.get("password")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")

        if month.isnumeric():
            month = int(month)

        elif isinstance(month, str):
            month = datetime.datetime.strptime(month, '%B').month
        else:
            error = "Enter a valid Month."
            return render(request, 'home/signup.html', {"error": error, "user_type": user_type})
        password2 = request.POST.get("confirm_password")

        dob = datetime.datetime(year=int(year), month=month, day=int(day))

        test = User.objects.filter(email=email).first()
        if test:
            error = "User Already Exists."
            return render(request, 'home/signup.html', {"error": error, "user_type": user_type})

        if password1 == password2:
            user = User.objects.create_user(email=email, is_active=False, password=password1, first_name=first_name,
                                            last_name=last_name, address=address, phone=phone, dob=dob, gender=gender)
            return render(request, 'home/home.html', {})

        else:
            error = "Please enter the same password."
            return render(request, 'home/signup.html', {"error": error, "user_type": user_type})
    else:
        return render(request, 'home/signup.html', {"user_type": user_type})


class Authe(ModelBackend):
    def authenticate(request=None, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except UserModel.DoesNotExist:
            return None
def LoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(email,password)
        user = Authe.authenticate(request, username=email, password=password)
        print(f"User Details: {user}")

        if user:
            login(request, user)
            return render(request,'home/home.html')
        else:
            result = "Email or password does not match"
            return render(request, 'home/signin.html', {'results': result})

    else:
        return render(request, 'home/signin.html')


def Logout(request):
    logout(request)
    return redirect('home')


def Contact(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        try:
            ContactUs.objects.create(full_name=full_name, email=email, phone=phone, message=message)
            return redirect('home')
        except Exception as e:
            return render(request, 'home/contactus.html', {"error": str(e)})
    else:
        return render(request, 'home/contactus.html')


def UserAppointments(request):
    year = request.GET.get("year", "None")
    month = request.GET.get("month")
    day = request.GET.get("day")
    today = datetime.datetime.now()

    if year and month and day:
        today = str(month) + " " + str(day) + "," + str(year)
        month = datetime.datetime.strptime(month, '%B').month
        order = Order.objects.filter(user=request.user, appointment_start_time__year=year,
                                     appointment_start_time__month=month,
                                     appointment_start_time__day=day)
        context = {
            "today": today,
            "order": order
        }
    else:
        today = today.date()
        order = Order.objects.filter(user=request.user, appointment_start_time__date=today)

        context = {
            "today": today,
            "order": order
        }
    return render(request, "home/appointments.html", context=context)


def DeleteUser(request, id):
    User.objects.filter(id=id).update(is_delete=True)
    User.objects.filter(id=id).delete()
    return redirect("staff-list")


def ContactList(request):
    contact = ContactUs.objects.all()
    return render(request, "home/allcontactus.html", {"contactus": contact})


def ContactDelete(request, id):
    ContactUs.objects.filter(id=id).delete()
    return redirect("contactus")
