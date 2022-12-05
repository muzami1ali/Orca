from django_tables2 import MultiTableMixin
from django.views.generic.base import TemplateView
from lessons.tables import Lesson_Table,Lesson_Request_Table,Student_Table,Invoice_Table,Bank_Transfer_Table
from lessons.models import Lesson,LessonRequest,Student,Invoice,bankTransfers
import django_tables2 as tables




class AdminTableView(MultiTableMixin, TemplateView):
    template_name = "admin_panel.html"
    lesson_qs=Lesson.objects.all()
    lesson_request_qs=LessonRequest.objects.all()
    student_qs=Student.objects.all()
    invoice_qs=Invoice.objects.all()
    bank_transfer_qs=bankTransfers.objects.all()
    tables = [
        Lesson_Request_Table(lesson_request_qs),
        Lesson_Table(lesson_qs),
        Student_Table(student_qs),
        Invoice_Table(invoice_qs),
        Bank_Transfer_Table(bank_transfer_qs),
       
    ]

    table_pagination = {
        "per_page": 10
    }
class StudentTable(tables.SingleTableView):
    table_class = Student_Table
    queryset = Student.objects.all()
    template_name = "admin_panel.html"