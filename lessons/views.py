from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForms, LogInForm, LessonRequestForm, BankTransferForm
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
    if request.method == 'POST':
        if LessonRequest.objects.filter(id=LessonRequestID).exists():
            lesson_request = LessonRequest.objects.get(id=LessonRequestID)
            student_object = Student.objects.get(id=request.user.id)

            edit_form = EditBookedLessonForm(
                initial={
                    'first_name':student_object.first_name,
                    'last_name:':student_object.last_name,
                    'date':lesson_request.lesson.date
                    }
                )
        else:
            raise IntegrityError
    else:
        edit_form = EditBookedLessonForm()
    return render(request, 'edit_lesson.html', {'edit_lesson_form': edit_form, 'lessonID': LessonRequestID})

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
