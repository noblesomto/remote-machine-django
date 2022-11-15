from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, UserManager, auth
from django.contrib import messages
from django.http import HttpResponse
import random
from user.models import Notification, User, Machine
from .models import Requests, RequestImage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
            messages.info(request, 'Email Address is not correct or Does not exist')
            return redirect('/worker/login')
        if user:
            flag = check_password(password, user.password)
            if flag:
                request.session['user_id'] = user.id
                request.session['name'] = user.first_name
                request.session['user_category'] = user.user_category
                return redirect("/worker/dashboard")
            else:
                messages.info(request, 'Password is not correct')
                return redirect('/worker/login')
        else:
                messages.info(request, 'Sorry, we cannot get your details, please contact admin')
                return redirect('/worker/login')
    else:
        title = "Login"
        return render(request, 'frontend/worker/login.html', {'title': title})


def logout(request):
    request.session.clear()
    return redirect('/worker/login')


def dashboard(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.all().order_by('-id')
    paginator = Paginator(machine, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['user'] = user
    context['machine'] = page_obj
    context['title'] = "dashboard"
    return render(request, 'frontend/worker/dashboard.html', context)



def assistance(request, machine_id): 
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    
    context['user'] = user
    context['machine_id'] = machine_id
    context['title'] = "Request Assistance"
    if request.method == "POST":
        machine_id = request.POST['machine_id']
        subject = request.POST['subject']
        description = request.POST['description']
        req_id = random.randint(00000, 99999)
        request_type = "Maintanace"
        request_status = "Pending"
        post = Requests.objects.create(
            req_id=req_id, machine_id=Machine.objects.get(id=int(machine_id)), subject=subject, request_type=request_type,
            description=description, request_status=request_status)
        post.save()
        images = request.FILES.getlist('machine-image')
        for image in images:
            photo = RequestImage.objects.create(
                image=image,
                req_id=req_id,
            )

        messages.info(
            request, 'Request successfully Submited')
        return redirect('assistance', machine_id=machine_id)
    else:
        return render(request, 'frontend/worker/request-assistance.html', context)


def failure(request, machine_id): 
    context = {}
    context['machine_id'] = machine_id
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    
    context['user'] = user
    context['title'] = "Report Machine Failure"
    if request.method == "POST":
        machine_id = request.POST['machine_id']
        subject = request.POST['subject']
        description = request.POST['description']
        req_id = random.randint(00000, 99999)
        request_type = "Failure"
        request_status = "Pending"
        post = Requests.objects.create(
            req_id=req_id, machine_id=Machine.objects.get(id=int(machine_id)), subject=subject, request_type=request_type,
            description=description, request_status=request_status)
        post.save()
        images = request.FILES.getlist('machine-image')
        for image in images:
            photo = RequestImage.objects.create(
                image=image,
                req_id=req_id,
            )

        messages.info(
            request, 'Failure Report successfully Submited')
        return redirect('failure', machine_id=machine_id)
    else:
        return render(request, 'frontend/worker/failure-request.html', context)


def requests(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    
    context['user'] = user
    context['title'] = "dashboard"
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

    return render(request, 'frontend/worker/requests.html', context)


def request_details(request,id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
        
    req_id = id
    req = Requests.objects.get(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)

    context['user'] = user
    context['title'] = "Request Details"
    context['request'] = req
    context['image'] = image
    return render(request, 'frontend/worker/request-details.html', context)


def contact(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    posts = Requests.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['user'] = user
    context['request'] = page_obj
    context['title'] = "dashboard"
    return render(request, 'frontend/worker/contact.html', context)



def notification(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    posts = Notification.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['user'] = user
    context['notification'] = page_obj
    context['title'] = "Notification"
    return render(request, 'frontend/worker/notification.html', context)


def experts(request, id):
    req_id = id
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    expert = User.objects.filter(user_category="Expert")
    
    context['user'] = user
    context['expert'] = expert
    context['req_id'] = req_id
    context['title'] = "Chat with Expert"
    return render(request, 'frontend/worker/experts.html', context)


def serviceman(request, id):
    req_id = id
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    serviceman = User.objects.filter(user_category="Serviceman")
    
    context['user'] = user
    context['serviceman'] = serviceman
    context['req_id'] = req_id
    context['title'] = "dashboard"
    return render(request, 'frontend/worker/serviceman.html', context)


def chat(request, id, req_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    userchat = User.objects.get(user_id=id)
    req = Requests.objects.get(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)

    context['user'] = user
    context['userchat'] = userchat
    context['req'] = req
    context['image'] = image
    context['title'] = "Chat"
    return render(request, 'frontend/worker/chat.html', context)


def logout(request):
    request.session.clear()
    return redirect('login')