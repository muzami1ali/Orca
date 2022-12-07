from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForms, LogInForm, LessonRequestForm, BankTransferForm
from django.contrib import messages
from .models import Lesson, LessonRequest, Student, Invoice
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Max
import lessons.views_folder.AdminPanel as admin


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
