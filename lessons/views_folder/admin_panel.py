
from lessons.models import Lesson,LessonRequest,Student,Invoice,BankTransfer
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages


@login_required(login_url='log_in')
def admin_panel(request):
    if request.method=="POST":
        return redirect('admin_panel')
    else:
        lesson_request = LessonRequest.objects.filter(is_authorised=False).all()
        invoice=Invoice.objects.filter(is_fulfilled=False).all()
        bank_transfer=BankTransfer.objects.filter(is_approved=False).all()
        return render(request,'admin_panel.html', {'lesson_request': lesson_request,'invoices':invoice,'bank_transfer':bank_transfer})

@login_required(login_url='log_in')
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

@login_required(login_url='log_in')
def approve_bank_payment(request,BankTransferID):
    # current_user=request.user
    # bank_transfer=BankTransfer.objects.filter(id=BankTransferID).get()
    # # inv=Invoice.objects.filter(invoice=bank_transfer.invoice).get()
    # if bank_transfer.amount==50:
    #     bank_transfer.update(is_approved=True)
    #     # inv.update(is_fulfilled=True)
    #     messages.success(request, 'Payment approved successfully')
        pass
    # return redirect('admin_panel')

