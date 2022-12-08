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
    if Invoice.objects.filter(student_id=request.user.id).filter(is_fulfilled=False).exists():
        invoices = Invoice.objects.filter(student_id=request.user.id).filter(is_fulfilled=False)
        totalPrice = 50 * len(invoices)
        return render(request, 'invoice.html', {'invoices':invoices, 'totalPrice': totalPrice})
    else:
        message = "No invoices available."
        totalPrice = 0
        return render(request, 'invoice.html', {'message': message, 'totalPrice': totalPrice})
