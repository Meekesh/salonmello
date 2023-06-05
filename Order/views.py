from django.shortcuts import render,redirect
from .models import Order
from Common.models import ConfigChoice
from django.contrib.auth.decorators import login_required
from Services.models import Service
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
@login_required(login_url="login")
def CreateAppointment(request):
    check=datetime.today()


    categorys = ConfigChoice.objects.filter(category__name="Service", is_active=True)
    services = Service.objects.filter(is_deleted=False)
    user = User.objects.filter(is_delete=False)
    context = {
        "service": services,
        "users": user,
        "category": categorys
    }
    if request.method == 'POST':
        service = request.POST.get('service')
        service = Service.objects.get(id=service)
        year = request.POST.get('year')
        month = request.POST.get('month')
        month = datetime.strptime(month, '%B').month

        date = request.POST.get('date')
        time = request.POST.get("time")
        date=str(year)+'-'+str(month)+"-"+str(date)+"T"+str(time)+":00"
        start_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        end_date = start_date+timedelta(hours=service.duration)

        if check>start_date:
            context["error"] = "Enter a Valid Date"
            return render(request, 'home/newappointments.html', context=context)


        order=Order.objects.filter(service=service)

        Order.objects.create(user=request.user, service=service,
                             appointment_start_time=start_date, appointment_end_time=end_date)
        if request.user.user_type.name == "Super User":
            return redirect("superadmin-appointments")
        else:
            return redirect("user-appointments")
    else:
        return render(request, 'home/newappointments.html', context=context)