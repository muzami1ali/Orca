from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LogInForm


def home(request):
    return render(request,'index.html')


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('booking')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

    #return render(request,'log_in.html')

def booking(request):
    return render(request,'booking.html')
