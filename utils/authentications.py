
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User



def login_page(request):
    return render(request, "login.html")

def handleLogin(request):
    if request.user.is_authenticated:
        return redirect('/start_strategy')

    if request.method == "POST":
        loginusername = request.POST['username']
        loginpassword = request.POST['password']
        if loginusername=="bybit_bot" and loginpassword=="bot_to_trade":
            user=User.objects.get(username=loginusername)
            login(request, user)
            return redirect("../start_strategy/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")
    return redirect("/")


@login_required(login_url='')
def handleLogout(request):
    logout(request)
    return redirect('/')

