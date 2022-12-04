from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForms, LogInForm, LessonRequestForm, BankTransferForm
from django.contrib import messages
from .models import Lesson, LessonRequest, Student, Invoice, InvoiceNumber
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Max



def home(request):
    return render(request,'index.html')

def booking(request):
    return render(request,'booking.html')
    
@login_required(login_url='log_in')
def contact(request):
    return render(request,'contact.html')



def getRefNumber(student_id):
    InvoiceNumber.objects.create()
    max = str(InvoiceNumber.objects.all().aggregate(Max('id')).get('id__max')).zfill(3)
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
def request_lessons(request):
    if request.method == "POST":
        if LessonRequest.objects.filter(student_id=request.user.id).exists():
            try:
                student_booked_lessons = LessonRequest.objects.filter(student_id=request.user.id)
                duplicate_lesson = False

                for lesson_request in student_booked_lessons:
                    lesson = Lesson.objects.get(id=lesson_request.lesson_id)
                    if lesson.equal_to(request):
                        duplicate_lesson = True
                        break

                if not duplicate_lesson:
                    book_lesson = LessonRequestForm(request.POST)
                    book_lesson = book_lesson.save()
                    LessonRequest.objects.create(student_id=request.user.id, lesson_id=book_lesson.id)
                else:
                    raise IntegrityError("Class cannot be booked twice")
            except ValueError:
                pass
        else:
            try:
                book_lesson = LessonRequestForm(request.POST)
                book_lesson = book_lesson.save()
                LessonRequest.objects.create(student_id=request.user.id, lesson_id=book_lesson.id)
            except IntegrityError:
                pass
        return redirect('request_lessons')
    else:
        form = LessonRequestForm()
        return render(request, 'request_lessons.html', {'lesson_form': form})

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
    invoices = Invoice.objects.all()
    totalPrice = 50 * len(invoices)
    return render(request, 'invoice.html', {'invoices':invoices, 'totalPrice': totalPrice})

def admin_panel(request):
    context={
        'lessons_request_data':LessonRequest.objects.all(),
        'user_data':Student.objects.all(),
        'lessons_data':Lesson.objects.all()
    }
    return render(request,'admin_panel.html',context)
