'''
    LessonRequest contains the views for requesting lessons as a student.
    @author Dean Whitbread
    @version 02/12/2022
'''
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from lessons.models import Lesson, LessonRequest,Invoice
from lessons.forms import LessonRequestForm


@login_required(login_url='log_in')
def request_lessons(request):
    if request.method == "POST":
        if LessonRequest.objects.filter(student_id=request.user.id).exists():
            try:
                student_booked_lessons = LessonRequest.objects.filter(student_id=request.user.id)
                duplicate_lesson = False

                for lesson_request in student_booked_lessons:
                    lesson = Lesson.objects.get(id=lesson_request.lesson_id)
                    if lesson.equal_to(request):
                        duplicate_lesson = True
                        break

                if not duplicate_lesson:
                    book_lesson = LessonRequestForm(request.POST)
                    book_lesson = book_lesson.save()
                    lesson_rq=LessonRequest.objects.create(student_id=request.user.id, lesson_id=book_lesson.id)
                    if lesson_rq.is_authorised==True:
                        rand_invoice=request.user.generate_invoice_number()
                        invoice_object=Invoice(student=request.user,lesson=book_lesson,invoice=rand_invoice)
                        invoice_object.save()
                else:
                    return HttpResponseBadRequest("Class cannot be booked twice.")
            except ValueError:
                return HttpResponseBadRequest("Cannot submit incomplete form.")
        else:
            try:
                book_lesson = LessonRequestForm(request.POST)
                book_lesson = book_lesson.save()
                lesson_rq=LessonRequest.objects.create(student_id=request.user.id, lesson_id=book_lesson.id)
                if lesson_rq.is_authorised==True:
                    rand_invoice=request.user.generate_invoice_number()
                    invoice_object=Invoice(student=request.user,lesson=book_lesson,invoice=rand_invoice)
                    invoice_object.save()
            except IntegrityError:
                return HttpResponseBadRequest("Lesson request does not exits.")
        return redirect('request_lessons')
    else:
        form = LessonRequestForm()
        return render(request, 'request_lessons.html', {'lesson_form': form})
