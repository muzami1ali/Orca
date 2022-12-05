import django_tables2 as tables
from lessons.models import Student,Lesson,LessonRequest,Invoice,bankTransfers

class Student_Table(tables.Table):
    class meta:
        model = Student
        
class Lesson_Table(tables.Table):
    class meta:
        model=Lesson

class Lesson_Request_Table(tables.Table):
    class meta:
        model=LessonRequest

class Invoice_Table(tables.Table):
    class meta:
        model=Invoice

class Bank_Transfer_Table(tables.Table):
    class meta:
        model=bankTransfers
        