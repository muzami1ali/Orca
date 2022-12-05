# from django_tables2 import MultiTableMixin
# from django.views.generic.base import TemplateView
from lessons.tables import Lesson_Table,Lesson_Request_Table,Student_Table,Invoice_Table,Bank_Transfer_Table
from lessons.models import Lesson,LessonRequest,Student,Invoice,bankTransfers
# import django_tables2 as tables
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect


@login_required(login_url='log_in')
def admin_panel(request):
    if request.method=="POST":
        return redirect('admin_panel')
    else:
        lesson_request = LessonRequest.objects.filter(is_authorised=False).all()
        invoice=Invoice.objects.all()
        bank_transfer=bankTransfers.objects.all()
        return render(request,'admin_panel.html', {'lesson_request': lesson_request,'invoice':invoice,'bank_transfer':bank_transfer})

# class AdminTableView(MultiTableMixin, TemplateView):
#     template_name = "admin_panel.html"
#     lesson_qs=Lesson.objects.all()
#     lesson_request_qs=LessonRequest.objects.all()
#     student_qs=Student.objects.all()
#     invoice_qs=Invoice.objects.all()
#     bank_transfer_qs=bankTransfers.objects.all()
#     tables = [
#         Lesson_Request_Table(lesson_request_qs),
#         Lesson_Table(lesson_qs),
#         Student_Table(student_qs),
#         Invoice_Table(invoice_qs),
#         Bank_Transfer_Table(bank_transfer_qs),
       
#     ]

#     table_pagination = {
#         "per_page": 10
#     }
