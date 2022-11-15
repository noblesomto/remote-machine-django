from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, UserManager, auth
from django.contrib import messages
from django.http import HttpResponse
import random
from user.models import Notification, User, Machine
from .models import Instruction
from worker.models import Requests, RequestImage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator




def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            user = None
            messages.info(request, 'Email Address is not correct or Does not exist')
            return redirect('/expert/login')
        if user:
            flag = check_password(password, user.password)
            if flag:
                request.session['user_id'] = user.user_id
                request.session['name'] = user.first_name
                request.session['user_category'] = user.user_category
                return redirect("/expert/dashboard")
            else:
                messages.info(request, 'Password is not correct')
                return redirect('/expert/login')
        else:
                messages.info(request, 'Sorry, we cannot get your details, please contact admin')
                return redirect('/expert/login')
    else:
        title = "Login"
        return render(request, 'frontend/expert/login.html', {'title': title})


def logout(request):
    request.session.clear()
    return redirect('/expert/login')


def dashboard(request):
    context = {}
    user_id = request.session.get('user_id')
    user = Users.objects.get(user_id=user_id)
    machine = Machine.objects.all().order_by('-id')
    paginator = Paginator(machine, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['user'] = user
    context['machine'] = page_obj
    context['title'] = "dashboard"
    return render(request, 'frontend/expert/dashboard.html', context)


def give_instruction(request, machine_id): 
    context = {}
    user_id = request.session.get('user_id')
    user = Users.objects.get(user_id=user_id)
    
    context['user'] = user
    context['machine_id'] = machine_id
    context['title'] = "Give New Instruction"
    if request.method == "POST":
        machine_id = machine_id
        in_id = random.randint(00000, 99999)
        x_axis = request.POST['x_axis']
        y_axis = request.POST['y_axis']
        z_axis = request.POST['z_axis']
        machine_speed = request.POST['machine_speed']
        angle = request.POST['angle']
        post = Instruction.objects.create(
            in_id=in_id, machine_id=machine_id, x_axis=x_axis,
            y_axis=y_axis, z_axis=z_axis, machine_speed=machine_speed, angle=angle)
        post.save()
        
        messages.info(
            request, 'Instruction successfully Submited')
        return redirect('give_instruction', machine_id=machine_id)
    else:
        return render(request, 'frontend/expert/new-instruction.html', context)


def monitor_machine(request, machine_id):
    context = {}
    user_id = request.session.get('user_id')
    user = Users.objects.get(user_id=user_id)
    machine = Machine.objects.get(machine_id=machine_id)
    
    context['user'] = user
    context['machine'] = machine
    context['title'] = "Status Report"
    return render(request, 'frontend/expert/monitor-machine.html', context)


def maintenance(request, machine_id): 
    context = {}
    user_id = request.session.get('user_id')
    user = Users.objects.get(user_id=user_id)
    
    context['user'] = user
    context['machine_id'] = machine_id
    context['title'] = "Request Maintanace"
    if request.method == "POST":
        subject = request.POST['subject']
        description = request.POST['description']
        req_id = random.randint(00000, 99999)
        machine_id = machine_id
        request_type = "Maintanace"
        request_status = "Pending"
        post = Requests.objects.create(
            req_id=req_id, machine_id=machine_id, subject=subject, request_type=request_type,
            description=description, request_status=request_status)
        post.save()

        not_id = random.randint(00000, 99999)
        not_status = "Active"
        request_type = "maintenance"
        title = "Machine no #" + machine_id
        notification = Notification.objects.create(
            not_id=not_id, machine_id=machine_id, request=request_type, title=title, description=description,
            not_status=not_status)
        notification.save()

        images = request.FILES.getlist('machine-image')
        for image in images:
            photo = RequestImage.objects.create(
                image=image,
                req_id=req_id,
            )

        messages.info(
            request, 'Request successfully Submited')
        return redirect('expert/requests',)
    else:
        return render(request, 'frontend/expert/request-maintenance.html', context)


def requests(request):
    context = {}
    user_id = request.session.get('user_id')
    user = Users.objects.get(user_id=user_id)
    
    context['user'] = user
    context['title'] = "Requests"
    solved_request = Requests.objects.filter(request_status="Solved").order_by('-id')
    solved_paginator = Paginator(solved_request, 20)
    solved_page_number = request.GET.get('page')
    solved_page = solved_paginator.get_page(solved_page_number)
    context['solved_request'] = solved_page

    unsolved_request = Requests.objects.filter(request_status="Pending").order_by('-id')
    unsolved_paginator = Paginator(unsolved_request, 20)
    unsolved_page_number = request.GET.get('page')
    unsolved_page = unsolved_paginator.get_page(unsolved_page_number)
    context['unsolved_request'] = unsolved_page

    return render(request, 'frontend/expert/requests.html', context)


def request_details(request,id):
    context = {}
    user_id = request.session.get('user_id')
    user = Users.objects.get(user_id=user_id)
        
    req_id = id
    req = Requests.objects.get(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)

    context['user'] = user
    context['title'] = "Request Details"
    context['request'] = req
    context['image'] = image
    return render(request, 'frontend/expert/request-details.html', context)


def contact(request):
    context = {}
    user_id = request.session.get('user_id')
    user = Users.objects.get(user_id=user_id)

    posts = Requests.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['user'] = user
    context['request'] = page_obj
    context['title'] = "dashboard"
    return render(request, 'frontend/expert/contact.html', context)


def notification(request):
    context = {}
    user_id = request.session.get('user_id')
    user = Users.objects.get(user_id=user_id)
    posts = Notification.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['user'] = user
    context['notification'] = page_obj
    context['title'] = "Notification"
    return render(request, 'frontend/expert/notification.html', context)

def workers(request, id):
    req_id = id
    context = {}
    user_id = request.session.get('user_id')
    user = Users.objects.get(user_id=user_id)

    worker = Users.objects.filter(user_category="Worker")
    
    context['user'] = user
    context['worker'] = worker
    context['req_id'] = req_id
    context['title'] = "Chat with Worker"
    return render(request, 'frontend/expert/workers.html', context)


def serviceman(request, id):
    req_id = id
    context = {}
    user_id = request.session.get('user_id')
    user = Users.objects.get(user_id=user_id)

    serviceman = Users.objects.filter(user_category="Serviceman")
    
    context['user'] = user
    context['serviceman'] = serviceman
    context['req_id'] = req_id
    context['title'] = "dashboard"
    return render(request, 'frontend/worker/serviceman.html', context)


def chat(request, id, req_id):
    context = {}
    user_id = request.session.get('user_id')
    user = Users.objects.get(user_id=user_id)

    userchat = Users.objects.get(user_id=id)
    req = Requests.objects.get(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)

    context['user'] = user
    context['userchat'] = userchat
    context['req'] = req
    context['image'] = image
    context['title'] = "Chat"
    return render(request, 'frontend/worker/chat.html', context)