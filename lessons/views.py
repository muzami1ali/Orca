from django.shortcuts import render
from .forms import SignUpForms

def home(request):
    return render(request,'index.html')


def sign_up(request):
    
    context={}
    context['form']=SignUpForms()
    return render(request, 'sign_up.html', context)
