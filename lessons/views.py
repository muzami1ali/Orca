from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForms, LogInForm, LessonRequestForm, BankTransferForm
from django.contrib import messages
from .models import Lesson, LessonRequest, Student
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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
                    return HttpResponseBadRequest("Class cannot be booked twice")
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

@login_required(login_url='/log_in/')
def request_status(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            request_status = LessonRequest.objects.filter(student=request.user)
            lesson_counter = LessonRequest.objects.filter(student=request.user).count()
            return render(request, 'request_status.html', {'request_status': request_status, 'lesson_counter': lesson_counter})
    else:
        return redirect('log_in')


@login_required(login_url='/log_in/')
def edit_lesson(request, LessonRequestID):
    if request.method == 'POST':
        try:
            if request.user.id == LessonRequest.objects.get(id=LessonRequestID).student_id:
                lesson_request = LessonRequest.objects.filter(id=LessonRequestID).get()
                booked_lesson = Lesson.objects.filter(id=lesson_request.lesson_id).update(
                    lesson_name = request.POST.get('lesson_name'),
                    student_availability = request.POST.get('student_availability'),
                    number_of_lessons = request.POST.get('number_of_lessons'),
                    interval = request.POST.get('interval'),
                    duration = request.POST.get('duration'),
                    term_period = request.POST.get('term_period'),
                    additional_information = request.POST.get('additional_information')
                )
            else:
                return HttpResponseForbidden("Cannot edit other student lesson requests")
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Lesson request does not exist.")
        except MultipleObjectsReturned:
            return HttpResponseBadRequest("Multiple lesson objects found.")

        return redirect('request_status')
    else:
        if LessonRequest.objects.filter(id=LessonRequestID).exists():
            if request.user.id == LessonRequest.objects.get(id=LessonRequestID).student_id:
                lesson_request = LessonRequest.objects.get(id=LessonRequestID)
                edit_form = LessonRequestForm(
                    initial={
                        'lesson_name':lesson_request.lesson.lesson_name,
                        'student_availability':lesson_request.lesson.student_availability,
                        'number_of_lessons':lesson_request.lesson.number_of_lessons,
                        'interval':lesson_request.lesson.interval,
                        'duration':lesson_request.lesson.duration,
                        'term_period':lesson_request.lesson.term_period,
                        'additional_information':lesson_request.lesson.additional_information,
                        }
                    )
            else:
                return HttpResponseForbidden("Cannot edit other student lesson requests")
        else:
            return HttpResponseForbidden("Cannot edit this lesson request.")
    return render(request, 'edit_lesson.html', {'edit_lesson_form': edit_form, 'lessonID': LessonRequestID})

@login_required(login_url='/log_in/')
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
                return HttpResponseForbidden("Cannot cancel lesson booked by another student.")
        else:
            return HttpResponseBadRequest("Cannot cancel the same booking twice.")
    return redirect('request_status')
