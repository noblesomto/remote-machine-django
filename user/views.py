from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, UserManager, auth
from django.contrib import messages
from django.http import HttpResponse
import random
from user.models import Notification, User, Machine
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


@login_required(login_url='/page/admin')
def dashboard(request):

    context = {}
    context['title'] = "Admin Dashboard"
    return render(request, 'backend/index.html', context)


@login_required(login_url='/page/admin')
def new_user(request):
    if request.method == "POST" and request.FILES['user_picture']:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_picture = request.FILES['user_picture']
        email = request.POST['email']
        phone = request.POST['phone']
        user_category = request.POST['user_category']
        user_status = "Active"
        password = make_password(phone, None, 'md5')
        user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email,
            user_category=user_category, phone=phone, password=password, user_picture=user_picture, user_status=user_status)
        user.save()

        messages.info(
            request, 'User Profile was successfully Created')
        return redirect('new_user')

    else:
        title = "New User"
        return render(request, 'backend/new-user.html', {'title': title})


@login_required(login_url='/page/admin')
def all_users(request):
    title = "All User"
    user = User.objects.all().order_by('-id')
    paginator = Paginator(user, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'backend/all-users.html', {'title': title, 'user': page_obj})



@login_required(login_url='/page/admin')
def edit_user(request, id):
    user_id = id
    users = User.objects.get(user_id=id)
    if request.method == "POST" and request.FILES['user_picture']:
        users.first_name = request.POST['first_name']
        users.last_name = request.POST['last_name']
        users.user_picture = request.FILES['user_picture']
        users.email = request.POST['email']
        users.phone = request.POST['phone']
        users.user_category = request.POST['user_category']
        users.save()

        messages.info(
            request, 'User was Edited successful')
        return redirect('edit_user', id=users.user_id)

    else:
        title = "Edit User"
        return render(request, 'backend/edit-user.html', {'title': title, 'user': users})


@login_required(login_url='/page/admin')
def user_status(request, id, status):
    user_id = id
    users = User.objects.get(user_id=id)
    users.user_status = status
    users.save()

    messages.info(
        request, 'User status was Edited successful')
    return redirect('all_users')


@login_required(login_url='/page/admin')
def new_machine(request):
    users = User.objects.filter(user_category="Expert")
    worker = User.objects.filter(user_category="Worker")
    if request.method == "POST" and request.FILES['machine_picture']:
        machine_name = request.POST['machine_name']
        machine_code = request.POST['machine_code']
        machine_picture = request.FILES['machine_picture']
        machine_expert = request.POST['machine_expert']
        machine_worker = request.POST['machine_worker']
        machine_type = request.POST['machine_type']
        machine_status = "Running"

        post = Machine.objects.create(
            machine_name=machine_name, machine_code=machine_code,
            machine_expert=User.objects.get(id=int(machine_expert)), machine_worker=User.objects.get(id=int(machine_worker)), machine_type=machine_type, machine_picture=machine_picture, machine_status=machine_status)
        post.save()

        messages.info(
            request, 'Machine information was successfully Created')
        return redirect('new_machine')

    else:
        title = "New Machine"
        return render(request, 'backend/machine/new-machine.html', {'title': title, 'user': users, 'worker':worker})


@login_required(login_url='/page/admin')
def all_machine(request):
    title = "All User"
    user = User.objects.all().order_by('-id')
    paginator = Paginator(user, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'backend/all-users.html', {'title': title, 'user': page_obj})



@login_required(login_url='/page/admin')
def new_notification(request):
    if request.method == "POST":
        request_type = request.POST['request']
        title = request.POST['title']
        description = request.POST['description']
        not_id = random.randint(00000, 99999)
        not_status = "Active"
        user = Notification.objects.create(
            not_id=not_id, request=request_type, title=title, description=description,not_status=not_status)
        user.save()

        messages.info(
            request, 'Notification was successfully Created')
        return redirect('new_notification')

    else:
        title = "New Notification"
        return render(request, 'backend/notification/new-notification.html', {'title': title})

@login_required(login_url='/page/admin')
def all_notification(request):
    title = "All User"
    user = User.objects.all().order_by('-id')
    paginator = Paginator(user, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'backend/all-users.html', {'title': title, 'user': page_obj})

@login_required(login_url='/page/admin')
def delete_user(request, id):
    users = User.objects.get(user_id=id)
    users.delete()
    return redirect('all_users')



def logout(request):
    auth.logout(request)
    return redirect('/')


