'''
    LessonRequest contains the views for requesting lessons as a student.
    @author Dean Whitbread
    @version 02/12/2022
'''
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, LessonRequest
from lessons.forms import LessonRequestForm
from lessons.views._HttpResponseConstantMsg import CANNOT_BOOK_TWICE_MSG

@login_required
def request_lessons(request):
    if request.method == "POST":
        if LessonRequest.objects.filter(student_id=request.user.id).exists():
            student_booked_lessons = LessonRequest.objects.filter(student_id=request.user.id)
            duplicate_lesson = False

            for lesson_request in student_booked_lessons:
                lesson = Lesson.objects.get(id=lesson_request.lesson_id)
                if lesson.equal_to(request):
                    duplicate_lesson = True
                    break

            if not duplicate_lesson:
                try:
                    book_lesson = LessonRequestForm(request.POST)
                    book_lesson = book_lesson.save()
                    LessonRequest.objects.create(student_id=request.user.id, lesson_id=book_lesson.id)
                except ValueError:
                    return HttpResponseBadRequest("Form cannot be incomplete.")
            else:
                return HttpResponseBadRequest("Class cannot be booked twice")

        else:
            try:
                book_lesson = LessonRequestForm(request.POST)
                book_lesson = book_lesson.save()
                LessonRequest.objects.create(student_id=request.user.id, lesson_id=book_lesson.id)
            except ValueError:
                return HttpResponseBadRequest("Form cannot be incomplete.")
        return redirect('request_lessons')
    else:
        form = LessonRequestForm()
        return render(request, 'request_lessons.html', {'lesson_form': form})
