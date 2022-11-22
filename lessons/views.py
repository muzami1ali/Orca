from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from .forms import SignUpForms

def home(request):
    return render(request,'index.html')



    
def sign_up(request):
    context={}
    if request.method =='POST':
        context['form']= SignUpForms(request.POST)
        if context['form'].is_valid():
            user=context['form'].save()
            login=(request,user)
            return redirect('sign_up')
    else:
        context['form'] =SignUpForms()
    return render(request,'sign_up.html',context)