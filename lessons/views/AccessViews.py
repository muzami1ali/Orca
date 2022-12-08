'''
AccessViews contains the views for log in, log out, and sign up.

@author
@version 07/12/2022
'''
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from lessons.forms import SignUpForms, LogInForm
from django.contrib import messages

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser or user.is_staff:
                    login(request,user)
                    return redirect('admin_panel')
                login(request, user)
                return redirect('request_lessons')
            messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

@login_required
def log_out(request):
    logout(request)
    return redirect('home')

def sign_up(request):
    context={}
    if request.method =='POST':
        context['form']= SignUpForms(request.POST)
        if context['form'].is_valid():
            context['form'].save()
            return redirect('login')
    else:
        context['form'] =SignUpForms()
    return render(request,'sign_up.html',context)
