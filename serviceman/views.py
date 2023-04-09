from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, UserManager, auth
from django.contrib import messages
from django.http import HttpResponse
import random
from user.models import Notification, User, Machine, Requests, RequestImage
from worker.models import Chat
from .models import Expert_chat
from worker.models import Serviceman_chat
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q




def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(Q(email=email) & Q(user_category="Serviceman"))
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

def get_notification(request):
    notification = Requests.objects.filter((Q(request_sender="Expert") | Q(request_type="Reminder")) & Q(serviceman_view="0")).count()
    return notification

def dashboard(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.filter(machine_serviceman=user_id).order_by('-id')
    paginator = Paginator(machine, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notification = get_notification(request)
    
    context['notification'] = notification
    context['user'] = user
    context['machine'] = page_obj
    context['title'] = "dashboard"
    return render(request, 'frontend/serviceman/dashboard.html', context)


def run_daignostics(request, id):
    machine_id = id
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = get_notification(request)
    
    context['notification'] = notification
    context['machine_id'] = machine_id
    context['user'] = user
    context['title'] = "dashboard"
    
    return render(request, 'frontend/serviceman/run-daignostics.html', context)

def request_assistance(request, machine_id): 
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
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
        request_sender = "Expert"
        post = Requests.objects.create(
            req_id=req_id, machine_id=Machine.objects.get(id=int(machine_id)), subject=subject, request_type=request_type,
            description=description,request_sender=request_sender, request_status=request_status)
        post.save()

        images = request.FILES.getlist('machine-image')
        for image in images:
            photo = RequestImage.objects.create(
                image=image,
                req_id=req_id,
            )

        not_status = "Active"
        request_type = "maintenance"
        not_sender = "Expert"
        title = "Machine no #" + machine_id
        notification = Notification.objects.create(
            machine_id=Machine.objects.get(id=int(machine_id)), request=request_type, title=title, description=description,
            not_status=not_status, not_id=Requests.objects.get(id=int(post.id)), not_sender=not_sender)
        notification.save()

        messages.info(
            request, 'Request successfully Submited')
        return redirect('maintenance', machine_id=machine_id)
    else:
        return render(request, 'frontend/expert/request-maintenance.html', context)


def start_monitoring(request, id):
    machine_id = id
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = get_notification(request)
    
    context['notification'] = notification
    context['machine_id'] = machine_id
    context['user'] = user
    context['title'] = "dashboard"
    
    return render(request, 'frontend/serviceman/start-monitoring.html', context)

def software_updates(request, id):
    machine_id = id
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = get_notification(request)
    
    context['notification'] = notification
    context['machine_id'] = machine_id
    context['user'] = user
    context['title'] = "dashboard"

    if request.method == "POST":
        
        messages.info(request, 'Software successfully Updated')
        return redirect('software_updates', id=machine_id)
    else:
    
        return render(request, 'frontend/serviceman/software-updates.html', context)


def requests(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    
    context['user'] = user
    context['title'] = "Requests"
    notification = get_notification(request)
    
    context['notification'] = notification
    unsolved_request = Requests.objects.filter(request_status="Pending").exclude(request_sender="Worker").order_by('-id')
    unsolved_paginator = Paginator(unsolved_request, 20)
    unsolved_page_number = request.GET.get('page')
    unsolved_page = unsolved_paginator.get_page(unsolved_page_number)
    context['unsolved_request'] = unsolved_page

    return render(request, 'frontend/serviceman/requests.html', context)

def solved_requests(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = get_notification(request)
    
    context['notification'] = notification
    context['user'] = user
    context['title'] = "Requests"
    solved_request = Requests.objects.filter(request_status="Solved").exclude(request_sender="Worker").order_by('-id')
    solved_paginator = Paginator(solved_request, 20)
    solved_page_number = request.GET.get('page')
    solved_page = solved_paginator.get_page(solved_page_number)
    context['solved_request'] = solved_page

    unsolved_request = Requests.objects.filter(request_status="Pending").order_by('-id')
    unsolved_paginator = Paginator(unsolved_request, 20)
    unsolved_page_number = request.GET.get('page')
    unsolved_page = unsolved_paginator.get_page(unsolved_page_number)
    context['unsolved_request'] = unsolved_page

    return render(request, 'frontend/serviceman/solved-requests.html', context)


def request_details(request,id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
        
    req_id = id
    req = Requests.objects.get(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)
    notification = get_notification(request)
    
    context['notification'] = notification
    context['user'] = user
    context['title'] = "Request Details"
    context['request'] = req
    context['image'] = image
    views = Requests.objects.get(req_id=req_id)
    views.serviceman_view = views.serviceman_view + 1
    views.save()

    return render(request, 'frontend/serviceman/request-details.html', context)


def contact(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    posts = Requests.objects.filter((Q(expert_status="Resolved") | Q(expert_status="Pending")) & Q(worker_status="Pending")).order_by('-id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notification = get_notification(request)
    
    context['notification'] = notification    
    context['user'] = user
    context['request'] = page_obj
    context['title'] = "dashboard"
    return render(request, 'frontend/serviceman/contact.html', context)


def notification(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    posts = Notification.objects.filter(Q(not_sender="Expert") | Q(request="reminder")).order_by('-id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notification = get_notification(request)
    
    context['notification'] = notification 
    context['user'] = user
    context['noti'] = page_obj
    context['title'] = "Notification"
    return render(request, 'frontend/serviceman/notification.html', context)

def chat(request, machine_id, req_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.get(id=machine_id)
    worker_id = machine.machine_worker_id
    expert_id = machine.machine_expert_id
    

    userchat = User.objects.get(id=expert_id)
    req = Requests.objects.get(req_id=req_id)
    chat = Expert_chat.objects.filter(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)
    req_id = req_id
    machine_id = machine_id
    notification = get_notification(request)
    
    context['notification'] = notification
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
        post = Expert_chat.objects.create(
            user_id=User.objects.get(id=int(user_id)), req_id=req_id, message=message)
        post.save()
        
        return redirect('chat', machine_id=machine_id, req_id=req_id)
    else:
        return render(request, 'frontend/serviceman/chat.html', context)


def chat_worker(request, machine_id, req_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.get(id=machine_id)
    worker_id = machine.machine_worker_id
    expert_id = machine.machine_expert_id
    

    userchat = User.objects.get(id=worker_id)
    req = Requests.objects.get(req_id=req_id)
    chat = Serviceman_chat.objects.filter(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)
    req_id = req_id
    machine_id = machine_id
    notification = get_notification(request)
    
    context['notification'] = notification
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
        post = Serviceman_chat.objects.create(
            user_id=User.objects.get(id=int(user_id)), req_id=req_id, message=message)
        post.save()
        
        return redirect('chat_worker', machine_id=machine_id, req_id=req_id)
    else:
        return render(request, 'frontend/serviceman/chat-worker.html', context)


def chat_expert(request, expert_id, machine_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.get(id=machine_id)
    chat = Expert_chat.objects.filter(machine_id=machine_id)
    userchat = User.objects.get(id=expert_id)
    notification = get_notification(request)
    
    context['notification'] = notification    
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

def video_call(request, id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    caller = User.objects.get(id=id)
    notification = get_notification(request)
    
    context['notification'] = notification
    context['user'] = user
    context['caller'] = caller
    context['title'] = "Video Call"
    return render(request, 'frontend/serviceman/video-call.html', context)


def video_call_2(request, id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    caller = User.objects.get(id=id)
    notification = get_notification(request)
    
    context['notification'] = notification
    context['user'] = user
    context['caller'] = caller
    context['title'] = "Video Call"
    return render(request, 'frontend/serviceman/video-call-2.html', context)


PER_PAGE = 8

def search(request, *args, **kwargs):

    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = get_notification(request)

    # Search
    search = ""
    if request.GET:
        search = request.GET.get('search', '')
        context['query'] = str(search)
    machine = Machine.objects.filter(
        machine_name__icontains=search) | Machine.objects.filter(
        machine_code__icontains=search).order_by('-id')

    # Pagination
    page = request.GET.get('page', 1)
    machine_paginator = Paginator(machine, PER_PAGE)
    try:
        machine = machine_paginator.page(page)
    except PageNotAnInteger:
        machine = machine_paginator.page(PER_PAGE)
    except EmptyPage:
        machine = machine_paginator.page(machine_paginator.num_pages)

    context['machine'] = machine
    context['title'] = "Search Result"
    context['notification'] = notification
    context['user'] = user

    return render(request, 'frontend/serviceman/search.html', context)