from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, UserManager, auth
from django.contrib import messages
from django.http import HttpResponse
import random
from django.contrib.auth.decorators import login_required


def index(request):
    title = "Home"

    return render(request, 'frontend/index.html', {'title': title})



def admin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session.set_expiry(86400)
            request.session['username'] = user.username
            return redirect('/users/dashboard')
        else:
            messages.info(request, 'Credentials are invalid')
            return redirect('/page/admin')
    else:
        title = "Login"
        return render(request, 'backend/login.html', {'title': title})