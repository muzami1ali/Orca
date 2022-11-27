from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForms, LogInForm, LessonRequestForm
from django.contrib import messages
from .models import Lesson, LessonRequest, Student
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied

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
                return redirect('booking')
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


@login_required
def request_lessons(request):
    choice_form = LessonRequestForm()
    lesson_counter = 0
    if request.method == 'POST':
        term_lesson = Lesson.objects.filter(term_period=request.POST['term_period'])
        lesson_counter = Lesson.objects.filter(term_period=request.POST['term_period']).count()
        choice_form = LessonRequestForm(request.POST)
        return render(request, 'request_lessons.html', {'choice_form' : choice_form, 'term_lessons' : term_lesson, 'lesson_counter': lesson_counter})
    return render(request, 'request_lessons.html', {'choice_form' : choice_form, 'lesson_counter': lesson_counter})

@login_required
def book_lesson(request, LessonID):
    if request.method == 'POST':
        if LessonRequest.objects.filter(student_id=request.user.id, lesson_id=LessonID).exists():
            raise IntegrityError("Class cannot be booked twice")
        else:
            try:
                LessonRequest.objects.create(student_id=request.user.id, lesson_id=LessonID)
            except IntegrityError:
                pass
    return redirect('request_lessons')

@login_required
def request_status(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            request_status = LessonRequest.objects.filter(student=request.user)
            lesson_counter = LessonRequest.objects.filter(student=request.user).count()
            return render(request, 'request_status.html', {'request_status': request_status, 'lesson_counter': lesson_counter})
    else:
        return redirect('log_in')


def edit_lesson(request, LessonRequestID):
    pass

@login_required
def cancel_lesson(request, LessonRequestID):
    if request.method == 'POST':
        lesson_request_object = LessonRequest.objects.filter(id=LessonRequestID)
        if lesson_request_object.exists():
            if (LessonRequest.objects.get(id=LessonRequestID)).student_id == request.user.id:
                try:
                    LessonRequest.objects.get(id=LessonRequestID).delete()
                except IntegrityError:
                    pass
            else:
                raise PermissionDenied("Cannot cancel lesson booked by another student.")
        else:
            raise IntegrityError("Cannot cancel booking twice.")
    return redirect('request_status')
