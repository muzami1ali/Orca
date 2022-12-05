from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForms, LogInForm, LessonRequestForm, BankTransferForm
from django.contrib import messages
from .models import Lesson, LessonRequest, Student, Invoice
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Max
import lessons.views_folder.admin_panel as admin


def home(request):
    return render(request,'index.html')

def booking(request):
    return render(request,'booking.html')
    
@login_required(login_url='log_in')
def contact(request):
    return render(request,'contact.html')



def getRefNumber(student_id):
    inv= Invoice.objects.create()
    max = str(Invoice.objects.all().aggregate(Max('id')).get('id__max')).zfill(3)
    return str(student_id).zfill(4) + "-" + max

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
            return redirect('log_in')
    else:
        context['form'] =SignUpForms()
    return render(request,'sign_up.html',context)


@login_required(login_url='log_in')
def bank_transfer(request):
    if request.method == 'POST':
        form= BankTransferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_transfer')
    else:
        form = BankTransferForm()
    return render(request, 'bank_transfer.html', {'form': form})

@login_required(login_url='log_in')
def invoice(request):
    use=request.user
    inv=Invoice.objects.all().get()
    invoices = Invoice.objects.filter(student_id=use.id).all()
    totalPrice = 50 * len(invoices)
    return render(request, 'invoice.html', {'invoices':invoices, 'totalPrice': totalPrice})

@login_required(login_url='log_in')
def deal_requests(request):
    lessonrequest = LessonRequest.objects.filter(is_authorised=False).all()
    return render(request, 'request_deal.html', {'lessonrequest': lessonrequest})

@login_required(login_url='log_in')
def authorise(request,nid):
    LessonRequest.objects.filter(id=nid).update(is_authorised=True)
    lr = LessonRequest.objects.filter(id=nid).first()
    Invoice.objects.create(student_id=lr.student.id, lesson_id=lr.lesson.id)
    return redirect('deal_requests')


@login_required(login_url='log_in')
def decline(request,nid):
    LessonRequest.objects.filter(id=nid).delete()
    return redirect('deal_requests')