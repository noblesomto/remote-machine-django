from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, UserManager, auth
from django.contrib import messages
from django.http import HttpResponse
import random
from user.models import Notification, User, Machine, Requests, RequestImage
from worker.models import Chat
from .models import Expert_chat
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q




def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(Q(email=email) & Q(user_category="Worker"))
        except User.DoesNotExist:
            user = None
            messages.info(request, 'Email Address is not correct or Does not exist')
            return redirect('/serviceman/login')
        if user:
            flag = check_password(password, user.password)
            if flag:
                request.session['user_id'] = user.id
                request.session['name'] = user.first_name
                request.session['user_category'] = user.user_category
                return redirect("/serviceman/dashboard")
            else:
                messages.info(request, 'Password is not correct')
                return redirect('/serviceman/login')
        else:
                messages.info(request, 'Sorry, we cannot get your details, please contact admin')
                return redirect('/serviceman/login')
    else:
        title = "Login"
        return render(request, 'frontend/serviceman/login.html', {'title': title})


def logout(request):
    request.session.clear()
    return redirect('/serviceman/login')


def dashboard(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.filter(machine_type="Machine").order_by('-id')
    paginator = Paginator(machine, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['user'] = user
    context['machine'] = page_obj
    context['title'] = "dashboard"
    return render(request, 'frontend/serviceman/dashboard.html', context)


def run_maintenance(request, machine_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.filter(machine_type="Machine").order_by('-id')
    paginator = Paginator(machine, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['user'] = user
    context['machine'] = page_obj
    context['title'] = "dashboard"
    return render(request, 'frontend/serviceman/run-maintenance.html', context)


def requests(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    
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

    return render(request, 'frontend/serviceman/requests.html', context)


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
    return render(request, 'frontend/serviceman/request-details.html', context)


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
    return render(request, 'frontend/serviceman/contact.html', context)


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
    return render(request, 'frontend/serviceman/notification.html', context)

def chat(request, machine_id, req_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.get(id=machine_id)
    worker_id = machine.machine_worker_id
    

    userchat = User.objects.get(id=worker_id)
    req = Requests.objects.get(req_id=req_id)
    chat = Chat.objects.filter(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)
    req_id = req_id
    machine_id = machine_id

    context['user'] = user
    context['userchat'] = userchat
    context['req'] = req
    context['chat'] = chat
    context['machine_id'] = machine_id
    context['image'] = image
    context['title'] = "Chat"
    if request.method == "POST":
        req_id = request.POST['req_id']
        message = request.POST['message']
        post = Chat.objects.create(
            user_id=User.objects.get(id=int(user_id)), req_id=req_id, message=message)
        post.save()
        
        return redirect('chat', machine_id=machine_id, req_id=req_id)
    else:
        return render(request, 'frontend/expert/chat.html', context)


def chat_expert(request, expert_id, machine_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.get(id=machine_id)
    chat = Expert_chat.objects.filter(machine_id=machine_id)
    userchat = User.objects.get(id=expert_id)
    

    context['user'] = user
    context['userchat'] = userchat
    context['machine_id'] = machine_id
    context['expert_id'] = expert_id
    context['machine'] = machine
    context['chat'] = chat
    context['title'] = "Chat"
    if request.method == "POST":
        machine_id = request.POST['machine_id']
        message = request.POST['message']
        post = Expert_chat.objects.create(
            user_id=User.objects.get(id=int(user_id)), machine_id=Machine.objects.get(id=int(machine_id)), message=message)
        post.save()
        
        return redirect('chat_expert', expert_id=expert_id, machine_id=machine_id)
    else:
        return render(request, 'frontend/serviceman/chat-expert.html', context)