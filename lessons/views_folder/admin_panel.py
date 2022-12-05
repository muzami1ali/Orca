
from lessons.models import Lesson,LessonRequest,Student,Invoice,BankTransfers

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect


@login_required(login_url='log_in')
def admin_panel(request):
    if request.method=="POST":
        return redirect('admin_panel')
    else:
        lesson_request = LessonRequest.objects.filter(is_authorised=False).all()
        invoice=Invoice.objects.all()
        bank_transfer=BankTransfers.objects.all()
        return render(request,'admin_panel.html', {'lesson_request': lesson_request,'invoices':invoice,'bank_transfer':bank_transfer})

@login_required
def approve_lesson(request,LessonRequestID):
    lesson_request=LessonRequest.objects.filter(id=LessonRequestID).update(is_authorised=True)
    return redirect('admin_panel')
