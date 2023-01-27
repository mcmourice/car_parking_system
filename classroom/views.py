from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView 
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .forms import CustomerForm, UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers
from django.conf import settings
from django.db.models import Q
import os
from .models import Customer,User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from datetime import datetime, date
from django.core.exceptions import ValidationError
from . import models
import operator
import itertools
from django.db.models import Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.hashers import make_password
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

def signup(request):
    return render(request, 'dashboard/login.html')


def home(request):
    return render(request, 'dashboard/login.html')


def dashboard(request):
    total_it = Customer.objects.aggregate(Sum("total_cost"))

    print(total_it.get("total_cost__sum"))
    total_it = total_it.get("total_cost__sum")

    total_cost = total_it

    cars = Customer.objects.all().count()
    users = User.objects.all().count()
    invoices = Customer.objects.filter(is_payed = False).count()

    context = {'total_cost':total_cost, 'users':users, 'cars':cars, 'invoices':invoices}
    return render(request, 'dashboard/dashboard.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_cashier:
                return redirect('dashboard')
            else:
                return redirect('login')
        else:
            messages.error(request, 'Wrong Username or Password')
            return redirect('home')        

def logout_view(request):
    logout(request)
    return redirect('/')                


def add_vehicle(request):
    choice = ["Black", "Gray", "Silver", "Red", "Blue","Other", 
            200, 300, 'Vehicle color']
    choice = {'choice':choice}
    return render(request, 'dashboard/add_vehicle.html', choice)

def search_item(request):
    if request.method=='POST':
        query = request.POST['query']
        results=Customer.objects.filter(
            Q(car_model__contains= query) | Q (license_plate__contains= query))
        return render(request, 'dashboard/search_item.html', {'query': query,'results':results})
    else:
        return render(request, 'dashboard/search_item.html',{})

def save_vehicle(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        car_model = request.POST['car_model']
        car_color = request.POST['car_color']
        email_add = request.POST['email_add']
        phone_number = request.POST['phone_number']
        comment = request.POST['comment']
        register_name = request.POST['register_name']
        license_plate = request.POST['license_plate']
        parking_space = request.POST['parking_space']
        parking_time = datetime.now()
        date_time = parking_time.strftime("%Y,%m,%d")
        
        a = Customer(first_name=first_name, last_name=last_name, phone_number= phone_number, email_add = email_add,
            car_model= car_model, car_color= car_color, license_plate=license_plate, 
            reg_date= date_time,register_name= register_name,comment= comment, parking_space = parking_space, parking_time = parking_time)
        a.save()
        messages.success(request, 'Vehicle registered successfully')
        return redirect('vehicle')
def update_vehicle (request, pk):
    vehicle=Customer.objects.get(id=pk)
    form = CustomerForm ()
    if request.method== 'POST':
        form=CustomerForm (request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle') 
    context= {'form':form}
    return render(request, 'dashboard/vehicle_table.html', context)
class ListVehicle(ListView):
    model = Customer
    template_name = 'dashboard/vehicles.html'
    context_object_name = 'customers'
    paginate_by = 5


    def get_queryset(self):
        return Customer.objects.filter(is_payed="True")


class UserView(ListView):
    model = User
    template_name = 'dashboard/list_user.html'
    context_object_name = 'users'
    paginate_by = 5
    def get_queryset(self):
        return User.objects.order_by('-id')



class Vehicle(ListView):
    model = Customer
    template_name = 'dashboard/list_vehicle.html'
    context_object_name = 'customers'
    paginate_by = 5
    def get_queryset(self):
        return Customer.objects.filter(is_payed="False")


class UserUpdateView(BSModalUpdateView):
    model = User
    template_name = 'dashboard/user_update.html'
    form_class = UserForm
    success_message = 'User details updated successfully.'
    success_url = reverse_lazy('users')



class VehicleReadView(BSModalReadView):
    model = Customer
    template_name = 'dashboard/view_vehicle.html'


class CarReadView(BSModalReadView):
    model = Customer
    template_name = 'dashboard/view_vehicle2.html'

class UserReadView(BSModalReadView):
    model = User
    template_name = 'dashboard/view_user.html'

class VehicleUpdateView(BSModalUpdateView):
    model = Customer
    template_name = 'dashboard/update_vehicle.html'
    form_class = CustomerForm
    success_url = reverse_lazy('vehicle')
    success_message = 'Vehicle details updated successfully.'

class CarUpdateView(BSModalUpdateView):
    model = Customer
    template_name = 'dashboard/update_vehicle2.html'
    form_class = CustomerForm
    success_url = reverse_lazy('listvehicle')
    success_message = 'Vehicle details updated successfully.'


class VehicleDeleteView(BSModalDeleteView):
    model = Customer
    template_name = 'dashboard/delete_vehicle.html'
    form_class = CustomerForm
    success_url = reverse_lazy('vehicle')
    success_message = 'Record deleted successfully.'


class CarDeleteView(BSModalDeleteView):
    model = Customer
    template_name = 'dashboard/delete_vehicle2.html'
    form_class = CustomerForm
    success_url = reverse_lazy('listvehicle')
    success_message = 'Record deleted successfully.'
 

def Pay(request, pk):
    Customer.objects.filter(id = pk).update(exit_time = datetime.now())
    Customer.objects.filter(id = pk).update(is_payed = "True")
    parking_time = Customer.objects.values_list('parking_time').filter(id = pk)
    exit_time = Customer.objects.values_list('exit_time').filter(id = pk)
    str_parking = str(parking_time)
    str_exit = str (exit_time)
    x = str_parking [44:53]
    y = str_exit [44:53]

    parking_time = datetime.strptime (x, "%H, %M, %S")
    exit_time = datetime.strptime (y, "%H, %M, %S")
    duration = exit_time-parking_time
    duration_hours = round(duration.seconds/3600,0)
    
    if duration_hours <= 5:
        total_cost = 100
        Customer.objects.filter(id = pk).update(total_cost = total_cost, 
        hours_spent = duration_hours)
        hours_spent = Customer.objects.values_list('hours_spent').filter(id = pk)
        messages.success(request, 'Payment successful')
        return redirect('listvehicle')  
    elif duration_hours <= 6:
        total_cost = 150
        Customer.objects.filter(id = pk).update(total_cost = total_cost, 
        hours_spent = duration_hours)
        hours_spent = Customer.objects.values_list('hours_spent').filter(id = pk)
        messages.success(request, 'Payment successful')
        return redirect('listvehicle')  
    elif duration_hours <= 7:
        total_cost = 250
        Customer.objects.filter(id = pk).update(total_cost = total_cost,
        hours_spent = duration_hours)
        hours_spent = Customer.objects.values_list('hours_spent').filter(id = pk)
        messages.success(request, 'Payment successful')
        return redirect('listvehicle')  
    elif duration_hours > 7:
        total_cost = 250 + (duration_hours - 7)*100
        Customer.objects.filter(id = pk).update(total_cost = total_cost, 
        hours_spent = duration_hours)
        hours_spent = Customer.objects.values_list('hours_spent').filter(id = pk)
        messages.success(request, 'Payment made successfully')
        return redirect('listvehicle')
    else:
        return 0

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



class GeneratePdf(ListView):
    def get(self, request, pk, *args, **kwargs):

        infos = Customer.objects.filter(id=pk).values('id','first_name','last_name', 'parking_space','email_add', 'total_cost','reg_date', 'hours_spent','parking_time', 'exit_time', 'card_number','register_name')
        print(infos)
        context = {
        "data": {
            'location': 'Thika Road, Nairobi',
            'address': 'P.O BOX 65071',
            'email': 'parking@gardencity.com',
        },
        "infos": infos,
        }

        pdf = render_to_pdf('dashboard/invoice.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
class ViewPdf(ListView):
    def get (self, request):
        datas = Customer.objects.filter(is_payed='True')
        context = {
        "data": {
            'location': 'Thika Road, Nairobi',
            'address': 'P.O BOX 65071',
            'email': 'parking@gardencity.com',
            'current_time': datetime.now().time(),
            'current_date': datetime.now().date(),
        },

        "datas": datas,
        }

        pdf = render_to_pdf('dashboard/vehicle_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
class PendingPdf(ListView):
    def get (self, request):
        unpaid_vehicles=Customer.objects.filter(is_payed="False")
        print(unpaid_vehicles)
        context = {
        "personal_data": {
            'today': 'Today', 
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
            'location': 'Thika Road, Nairobi',
            'address': 'P.O BOX 65071',
            'email': 'parking@gardencity.com',
            'current_time': datetime.now().time(),
            'current_date': datetime.now().date(),
        },

        "unpaid_vehicles": unpaid_vehicles,
        }

        pdf = render_to_pdf('dashboard/pending_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


class GeneratePDF(LoginRequiredMixin,ListView):
    def get(self, request, *args, **kwargs):
        template = get_template('invoice.html')
        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf('dashboard/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class DeleteUser(BSModalDeleteView):
    model = User
    template_name = 'dashboard/delete_user.html'
    success_message = 'Success: Data was deleted.'
    success_url = reverse_lazy('users')



def create(request):
    choice = ['1', '0', 5000, 10000, 15000, 'Register', 'Admin', 'Cashier']
    choice = {'choice': choice}
    if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            userType=request.POST['userType']
            email=request.POST['email']
            password=request.POST['password']
            password = make_password(password)
            if userType == "Register":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_register=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')
            elif userType == "Cashier":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_cashier=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')
            elif userType == "Admin":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')    
            else:
                messages.success(request, 'Member was not created')
                return redirect('users')
    else:
        choice = ['1', '0', 5000, 10000, 15000, 'Register', 'Admin', 'Cashier']
        choice = {'choice': choice}
        return render(request, 'dashboard/add.html', choice)














































































































































   



