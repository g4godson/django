from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    request.session['logged_in'] = -1
    return render(request, 'index.html')

def register(request):
    # if User.objects.filter(email = request.POST['email']):
    #     return redirect('/')
    msgs = User.objects.regValidator(request.POST)
    if msgs:
        print(msgs)
        for key,values in msgs.items():
            print("value : ",values,"key",key)
            messages.error(request, values, extra_tags = key)



        return redirect('/')
    else :
        password = request.POST['password']
        hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashedpw)
        request.session['logged_in'] = user.id
        request.session['status'] = "Registered"
        return redirect('/success')

def login(request):
    msgs = User.objects.loginValidator(request.POST)
    if msgs:
        for key,values in msgs.items():
            print("value : ",values,"key",key)
            messages.error(request, values, extra_tags = key)

        return redirect('/')

    else:
        users = User.objects.filter(email = request.POST['login_email'])
        request.session['logged_in'] = users[0].id
        request.session['status'] = "logged in"
        return redirect('/success')




def success(request):
    if request.session['logged_in']:

        context = {'user' : User.objects.get(id = request.session['logged_in']),
                    'status' : request.session['status'] }
        return render(request, 'success.html', context)
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')