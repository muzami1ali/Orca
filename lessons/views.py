from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForms, LogInForm, StudentLessonRequest
from django.contrib import messages
from .models import Lesson, LessonRequest
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
    choice_form = StudentLessonRequest()
    lesson_counter = 0
    if request.method == 'POST':
        term_lesson = Lesson.objects.filter(term_period=request.POST['term_period'])
        lesson_counter = Lesson.objects.filter(term_period=request.POST['term_period']).count()
        choice_form = StudentLessonRequest(request.POST)
        return render(request, 'student_request_lessons.html', {'choice_form' : choice_form, 'term_lessons' : term_lesson, 'lesson_counter': lesson_counter})
    return render(request, 'student_request_lessons.html', {'choice_form' : choice_form, 'lesson_counter': lesson_counter})

@login_required
def book_lesson(request, LessonID):
    if request.method == 'POST':
        try:
            book_lesson = LessonRequest(
                student=request.user,
                lesson=Lesson.objects.get(id=LessonID),
                is_authorised = False
            )
            book_lesson.save()
            Lesson.objects.get(id=LessonID).delete()
        except Lesson.DoesNotExist:
            pass
        except Lesson.MultipleObjectsReturned:
            pass
    return redirect('request_lessons')
