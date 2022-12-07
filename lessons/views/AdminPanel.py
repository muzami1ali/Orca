'''
AdminPanel contains the views for administartor and director views.

@author Harry Sharma
@version 06/12/2022
'''
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from lessons.models import Lesson, LessonRequest, Student, Invoice, BankTransfer
from django.http import  HttpResponseForbidden

@login_required
def admin_panel(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method=="POST":
            return redirect('admin_panel')
        else:
            lesson_request = LessonRequest.objects.all()
            invoice=Invoice.objects.all()
            bank_transfer=BankTransfer.objects.all()
            current_user=request.user
        
        return render(request,'admin_panel.html', {'lesson_request': lesson_request,'invoices':invoice,'bank_transfer':bank_transfer,'user':current_user})
    else:
        return redirect('request_lessons')       

@login_required
def approve_lesson(request,LessonRequestID):
    current_user = request.user
    chosen_lesson_request = LessonRequest.objects.filter(id=LessonRequestID).get()
    lesson_request = LessonRequest.objects.filter(id=LessonRequestID).update(is_authorised=True)
    user=chosen_lesson_request.student
    inv = Invoice(student=user, lesson=chosen_lesson_request.lesson,is_fulfilled=False)
    inv.save()
    reference=f'{user.id}-{inv.id}'
    inv.invoice=reference
    Invoice.objects.filter(id=inv.id).update(invoice=reference)
   
          
    return redirect('admin_panel')

@login_required
def delete_booking(request,LessonRequestID):
    lesson_request=LessonRequest.objects.filter(id=LessonRequestID).get()
    user=lesson_request.student
    lessons=lesson_request.lesson
    if lesson_request.is_authorised==False:
         LessonRequest.objects.filter(id=LessonRequestID).delete()
    else:
          LessonRequest.objects.filter(id=LessonRequestID).delete()
          Invoice.objects.filter(lesson=lessons,student=user).delete()
        
        
    return redirect('admin_panel')

@login_required
def approve_bank_payment(request,BankTransferID):
    bank_transfer=BankTransfer.objects.filter(id=BankTransferID).get()
    if bank_transfer.amount==50:
        BankTransfer.objects.filter(id=BankTransferID).update(is_approved=True)
        Invoice.objects.filter(invoice=bank_transfer.invoice).update(is_fulfilled=True)
    return redirect('admin_panel')
