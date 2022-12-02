from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForms, LogInForm, LessonRequestForm, BankTransferForm
from django.contrib import messages
from .models import Lesson, LessonRequest, Student
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def home(request):
    return render(request,'index.html')

def booking(request):
    return render(request,'booking.html')



def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('request_lessons')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

def sign_up(request):
    context={}
    if request.method =='POST':
        context['form']= SignUpForms(request.POST)
        if context['form'].is_valid():
            context['form'].save()
            return redirect('sign_up')
    else:
        context['form'] =SignUpForms()
    return render(request,'sign_up.html',context)


# @login_required(login_url='log_in')
# def request_lessons(request):
#     if request.method == "POST":
#         if LessonRequest.objects.filter(student_id=request.user.id).exists():
#             try:
#                 student_booked_lessons = LessonRequest.objects.filter(student_id=request.user.id)
#                 duplicate_lesson = False
#
#                 for lesson_request in student_booked_lessons:
#                     lesson = Lesson.objects.get(id=lesson_request.lesson_id)
#                     if lesson.equal_to(request):
#                         duplicate_lesson = True
#                         break
#
#                 if not duplicate_lesson:
#                     book_lesson = LessonRequestForm(request.POST)
#                     book_lesson = book_lesson.save()
#                     LessonRequest.objects.create(student_id=request.user.id, lesson_id=book_lesson.id)
#                 else:
#                     return HttpResponseBadRequest("Class cannot be booked twice")
#             except ValueError:
#                 pass
#         else:
#             try:
#                 book_lesson = LessonRequestForm(request.POST)
#                 book_lesson = book_lesson.save()
#                 LessonRequest.objects.create(student_id=request.user.id, lesson_id=book_lesson.id)
#             except IntegrityError:
#                 pass
#         return redirect('request_lessons')
#     else:
#         form = LessonRequestForm()
#         return render(request, 'request_lessons.html', {'lesson_form': form})

@login_required
def bank_transfer(request):
    if request.method == 'POST':
        form= BankTransferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_transfer')
    else:
        form = BankTransferForm()
    return render(request, 'bank_transfer.html', {'form': form})
