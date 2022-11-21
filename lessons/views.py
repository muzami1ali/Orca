from django.shortcuts import render

def home(request):
    return render(request,'index.html')


def sign_up(request):
    return render(request,'sign_up.html')
