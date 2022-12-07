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






@login_required(login_url='log_in')
def invoice(request):
    logged_in_user=request.user
    invoices = Invoice.objects.filter(student_id=logged_in_user.id).all()
    filter_invoices= invoices.filter(is_fulfilled = False).all()

    totalPrice = 50 * len(filter_invoices)
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
