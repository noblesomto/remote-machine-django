from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, UserManager, auth
from django.contrib import messages
from django.http import HttpResponse
import random
from user.models import Notification, User, Machine, Requests, RequestImage
from .models import Instruction
from serviceman.models import Expert_chat
from worker.models import  Chat
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q




def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(Q(email=email) & Q(user_category="Expert"))
        except User.DoesNotExist:
            user = None
            messages.info(request, 'Email Address is not correct or Does not exist')
            return redirect('/expert/login')
        if user:
            flag = check_password(password, user.password)
            if flag:
                request.session['user_id'] = user.id
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

def get_notification(request):
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    return notification

def get_ajax_notification(request):
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    return HttpResponse(notification)

def dashboard(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.all().order_by('-id')
    paginator = Paginator(machine, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()

    context['notification'] = notification
    context['user'] = user
    context['machine'] = page_obj
    context['title'] = "dashboard"
    return render(request, 'frontend/expert/dashboard.html', context)


def give_instruction(request, machine_id): 
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
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
            in_id=in_id, machine_id=Machine.objects.get(id=int(machine_id)), x_axis=x_axis,
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
    user = User.objects.get(id=user_id)
    machine = Machine.objects.get(id=machine_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['machine'] = machine
    context['title'] = "Status Report"

    return render(request, 'frontend/expert/monitor-machine.html', context)

def monitor_cobot(request, machine_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.get(id=machine_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['machine'] = machine
    context['title'] = "Status Report"

    return render(request, 'frontend/expert/monitor-cobot.html', context)


def machine_status(request, machine_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.get(id=machine_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['machine'] = machine
    context['title'] = "Machine Status"
    return render(request, 'frontend/expert/machine-status.html', context)


def maintenance(request, machine_id): 
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
        return render(request, 'frontend/expert/provide-assistance.html', context)

def request_maintenance(request, machine_id): 
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['machine_id'] = machine_id
    context['title'] = "Request Machine Maintanace"
    if request.method == "POST":
        subject = request.POST['subject']
        description = request.POST['description']
        req_id = random.randint(00000, 99999)
        machine_id = machine_id
        request_type = "Assistance"
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
        request_type = "assistance"
        not_sender = "Expert"
        title = "Machine no #" + machine_id
        notification = Notification.objects.create(
            machine_id=Machine.objects.get(id=int(machine_id)), request=request_type, title=title, description=description,
            not_status=not_status, not_id=Requests.objects.get(id=int(post.id)), not_sender=not_sender)
        notification.save()

        messages.info(
            request, 'Request successfully Submited')
        return redirect('request_maintenance', machine_id=machine_id)
    else:
        return render(request, 'frontend/expert/request-maintenance.html', context)


def requests(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['title'] = "Requests"
    solved_request = Requests.objects.filter(request_status="Solved").exclude(request_type="Reminder").order_by('-id')
    solved_paginator = Paginator(solved_request, 20)
    solved_page_number = request.GET.get('page')
    solved_page = solved_paginator.get_page(solved_page_number)
    context['solved_request'] = solved_page

    unsolved_request = Requests.objects.filter(request_status="Pending").exclude(request_type="Reminder").order_by('-id')
    unsolved_paginator = Paginator(unsolved_request, 20)
    unsolved_page_number = request.GET.get('page')
    unsolved_page = unsolved_paginator.get_page(unsolved_page_number)
    context['unsolved_request'] = unsolved_page

    return render(request, 'frontend/expert/requests.html', context)

def solved_requests(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['title'] = "Requests"
    solved_request = Requests.objects.filter(request_status="Solved").exclude(request_type="Reminder").order_by('-id')
    solved_paginator = Paginator(solved_request, 20)
    solved_page_number = request.GET.get('page')
    solved_page = solved_paginator.get_page(solved_page_number)
    context['solved_request'] = solved_page


    return render(request, 'frontend/expert/solved-requests.html', context)


def request_details(request,id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    req_id = id
    req = Requests.objects.get(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['title'] = "Request Details"
    context['request'] = req
    context['image'] = image
    views = Requests.objects.get(req_id=req_id)
    views.expert_view = views.expert_view + 1
    views.save()
    return render(request, 'frontend/expert/request-details.html', context)


def contact(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    posts = Requests.objects.filter((Q(expert_status="Resolved") | Q(expert_status="Pending")) & Q(worker_status="Pending")).exclude(request_type="Reminder").order_by('-id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['request'] = page_obj
    context['title'] = "Contact"
    return render(request, 'frontend/expert/contact.html', context)

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
    return render(request, 'frontend/expert/video-call.html', context)

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
    return render(request, 'frontend/expert/video-call-2.html', context)


def notification(request):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    posts = Notification.objects.exclude(Q(not_sender="Expert") | Q(request="reminder")).order_by('-id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['noti'] = page_obj
    context['title'] = "Notification"
    return render(request, 'frontend/expert/notification.html', context)

def workers(request, id):
    req_id = id
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    worker = User.objects.filter(user_category="Worker")
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['worker'] = worker
    context['req_id'] = req_id
    context['title'] = "Chat with Worker"
    return render(request, 'frontend/expert/workers.html', context)


def serviceman(request, id):
    req_id = id
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    serviceman = User.objects.filter(user_category="Serviceman")
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['serviceman'] = serviceman
    context['req_id'] = req_id
    context['title'] = "dashboard"
    return render(request, 'frontend/worker/serviceman.html', context)

def ajax_post_chat_2(request, machine_id, req_id):
    user_id = request.session.get('user_id')
    req_id = request.POST['req_id']
    message = request.POST['message']
    post = Chat.objects.create(
        user_id=User.objects.get(id=int(user_id)), req_id=req_id, message=message)
    post.save()

    return HttpResponse('Commented Successfully')


def ajax_chat_2(request, machine_id, req_id):
    """Render the chat"""
    
    queryset = Chat.objects.filter(req_id=req_id)
    # start the container chatbox div
    html = "<div class='chatboxes'>\n"
    first_person = queryset[0].user_id if queryset.exists() else None
    # fill the container div with live chatbox-n divs
    for chat in queryset:
        css_class = "chatbox-2" if chat.user_id == first_person else "chatbox-1"
        css_class_box = "chat-box-two-content" if chat.user_id == first_person else "chat-box-one-content"
        html += (
            f"""
                <div class='{css_class}'>
                    <div class={css_class_box}>
                        {chat.message}
                        <div class='text-right'>
                            <small>
                                {chat.chatday} <strong>at</strong> {chat.chatime}
                            </small>
                        </div>
                    </div>
                </div>
            """
        )
    # close the container chatbox div
    html += "</div>\n"
    return HttpResponse(html)

def chat_2(request, machine_id, req_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.get(id=machine_id)
    worker_id = machine.machine_worker_id
    expert_id = machine.machine_expert_id
    
    userchat = User.objects.get(id=worker_id)
    req = Requests.objects.get(req_id=req_id)
    chat = Chat.objects.filter(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)
    req_id = req_id
    machine_id = machine_id
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['userchat'] = userchat
    context['req'] = req
    context['chat'] = chat
    context['machine_id'] = machine_id
    context['expert_id'] = expert_id
    context['image'] = image
    context['title'] = "Chat"
    if request.method == "POST":
        req_id = request.POST['req_id']
        message = request.POST['message']
        post = Chat.objects.create(
            user_id=User.objects.get(id=int(user_id)), req_id=req_id, message=message)
        post.save()
        
        return redirect('chat_2', machine_id=machine_id, req_id=req_id)
    else:
        return render(request, 'frontend/expert/chat.html', context)

def expert_request_status(request,id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = Requests.objects.filter(worker_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    expert_status = request.POST['status']
    post = Requests.objects.get(req_id=id)
    post.expert_status = expert_status
    post.save()

    messages.info(request, 'Request status was Changed successfully')
    return redirect('/expert/contact')

def chat_serviceman(request, machine_id, req_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.get(id=machine_id)
    worker_id = machine.machine_worker_id
    serviceman_id = machine.machine_serviceman_id
    
    userchat = User.objects.get(id=serviceman_id)
    req = Requests.objects.get(req_id=req_id)
    chat = Expert_chat.objects.filter(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)
    req_id = req_id
    machine_id = machine_id
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
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
        
        return redirect('chat_serviceman', machine_id=machine_id, req_id=req_id)
    else:
        return render(request, 'frontend/expert/chat-serviceman.html', context)


def ajax_post_serviceman_chat_2(request, machine_id, req_id):
    user_id = request.session.get('user_id')
    req_id = request.POST['req_id']
    message = request.POST['message']
    post = Expert_chat.objects.create(
        user_id=User.objects.get(id=int(user_id)), req_id=req_id, message=message)
    post.save()

    return HttpResponse('Commented Successfully')


def ajax_serviceman_chat_2(request, machine_id, req_id):
    """Render the chat"""
    
    queryset = Expert_chat.objects.filter(req_id=req_id)
    # start the container chatbox div
    html = "<div class='chatboxes'>\n"
    first_person = queryset[0].user_id if queryset.exists() else None
    # fill the container div with live chatbox-n divs
    for chat in queryset:
        css_class = "chatbox-1" if chat.user_id == first_person else "chatbox-2"
        css_class_box = "chat-box-one-content" if chat.user_id == first_person else "chat-box-two-content"
        html += (
            f"""
                <div class='{css_class}'>
                    <div class={css_class_box}>
                        {chat.message}
                        <div class='text-right'>
                            <small>
                                {chat.chatday} <strong>at</strong> {chat.chatime}
                            </small>
                        </div>
                    </div>
                </div>
            """
        )
    # close the container chatbox div
    html += "</div>\n"
    return HttpResponse(html)

def define_program(request, id):
    machine_id = id
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['machine_id'] = machine_id
    context['user'] = user
    context['title'] = "dashboard"
    if request.method == "POST":
        request.session['x_axis'] = request.POST['x_axis']
        request.session['y_axis'] = request.POST['y_axis']
        request.session['z_axis'] = request.POST['z_axis']
        request.session['machine_speed'] = request.POST['machine_speed']
        request.session['angle'] = request.POST['angle']
        request.session['machine_id'] = request.POST['machine_id']
        
        return redirect('simulate_program', machine_id=machine_id)
    else:
        return render(request, 'frontend/expert/define-program.html', context)


def simulate_program(request, machine_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['machine_id'] = machine_id
    context['title'] = "dashboard"
    if request.method == "POST":
        request.session['x_axis'] = request.POST['x_axis']
        request.session['y_axis'] = request.POST['y_axis']
        request.session['z_axis'] = request.POST['z_axis']
        request.session['machine_speed'] = request.POST['machine_speed']
        request.session['angle'] = request.POST['angle']
        request.session['machine_id'] = request.POST['machine_id']
        
        return redirect('send_program', machine_id=machine_id)
    else:
        return render(request, 'frontend/expert/simulate-program.html', context)

def send_program(request, machine_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['machine_id'] = machine_id
    context['title'] = "dashboard"
    if request.method == "POST":
        del request.session['x_axis']
        del request.session['y_axis']
        del request.session['z_axis']
        del request.session['machine_speed']
        del request.session['angle']
        del request.session['machine_id']
        
        messages.info(request, 'Program successfully Sent')
        return redirect('define_program', id=machine_id)
    else:
        return render(request, 'frontend/expert/send-program.html', context)

def activate_webcam(request, machine_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    machine = Machine.objects.get(id=machine_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
    
    context['notification'] = notification
    context['user'] = user
    context['machine'] = machine
    context['title'] = "Status Report"
    return render(request, 'frontend/expert/activate-webcam.html', context)

def service_reminder(request, id): 
    context = {}
    context['machine_id'] = id
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = Requests.objects.filter(expert_view="0").exclude(Q(request_sender="Expert") | Q(request_type="Reminder")).count()
        
    context['notification'] = notification
    context['user'] = user
    context['title'] = "Send Service Reminder"
    if request.method == "POST":
        machine_id = request.POST['machine_id']
        subject = request.POST['subject']
        description = request.POST['description']
        req_id = random.randint(00000, 99999)
        request_type = "Reminder"
        request_status = "Pending"
        request_sender = "Worker"
        post = Requests.objects.create(
            req_id=req_id, machine_id=Machine.objects.get(id=int(machine_id)), subject=subject, request_type=request_type,
            description=description, request_status=request_status)
        post.save()
     
        not_status = "Active"
        request_type = "reminder"
        not_sender = "Worker"
        title = "Service Reminder"
        notification = Notification.objects.create(
            machine_id=Machine.objects.get(id=int(machine_id)), request=request_type, title=title, description=description,
            not_status=not_status, not_id=Requests.objects.get(id=int(post.id)), not_sender=not_sender)
        notification.save()

        messages.info(
            request, 'Service Reminder successfully Submited')
        return redirect('service_reminder', id=machine_id)
    else:
        return render(request, 'frontend/expert/service-reminder.html', context)

def machine_alarm(request, id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    notification = get_notification(request)

    context['notification'] = notification
    context['user'] = user
    context['title'] = "Machine Alarm"
    return render(request, 'frontend/expert/machine-alarm.html', context)

def logout(request):
    request.session.clear()
    return redirect('login')
