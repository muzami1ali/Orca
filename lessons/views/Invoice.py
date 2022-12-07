'''
Invoice contains the views for the invoice webpage and includes authorise, decline,
and a view to list the requests.

@author Xiangyi Li
@version 07/12/2022
'''
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from lessons.models import Invoice, LessonRequest

@login_required
def invoice(request):
    logged_in_user=request.user
    invoices = Invoice.objects.filter(student_id=logged_in_user.id).all()
    filter_invoices= invoices.filter(is_fulfilled = False).all()

    totalPrice = 50 * len(filter_invoices)
    return render(request, 'invoice.html', {'invoices':invoices, 'totalPrice': totalPrice})

@login_required
def deal_requests(request):
    lessonrequest = LessonRequest.objects.filter(is_authorised=False).all()
    return render(request, 'request_deal.html', {'lessonrequest': lessonrequest})

@login_required
def authorise(request,nid):
    LessonRequest.objects.filter(id=nid).update(is_authorised=True)
    lr = LessonRequest.objects.filter(id=nid).first()
    Invoice.objects.create(student_id=lr.student.id, lesson_id=lr.lesson.id)
    return redirect('deal_requests')


@login_required
def decline(request,nid):
    LessonRequest.objects.filter(id=nid).delete()
    return redirect('deal_requests')
