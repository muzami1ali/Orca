from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from .forms import SignUpForms

def home(request):
    return render(request,'index.html')



    
def sign_up(request):
    form =SignUpForms()
    if request.method == 'POST':
        form = SignUpForms(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('sign_up')
    return render(request, 'sign_up.html', {'form': form})


