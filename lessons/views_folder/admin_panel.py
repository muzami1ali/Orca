
from lessons.models import Lesson,LessonRequest,Student,Invoice,BankTransfer

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect


@login_required(login_url='log_in')
def admin_panel(request):
    if request.method=="POST":
        return redirect('admin_panel')
    else:
        lesson_request = LessonRequest.objects.filter(is_authorised=False).all()
        invoice=Invoice.objects.all()
        bank_transfer=BankTransfer.objects.all()
        return render(request,'admin_panel.html', {'lesson_request': lesson_request,'invoices':invoice,'bank_transfer':bank_transfer})

@login_required
def approve_lesson(request,LessonRequestID):
    current_user = request.user
    chosen_lesson_request = LessonRequest.objects.filter(id=LessonRequestID).get()
    lesson_request = LessonRequest.objects.filter(id=LessonRequestID).update(is_authorised=True)
    invoice_number = current_user.generate_invoice_number()
    user=chosen_lesson_request.student
    invoice = Invoice(student=user, lesson=chosen_lesson_request.lesson, invoice=invoice_number)
    invoice.save()
    return redirect('admin_panel')