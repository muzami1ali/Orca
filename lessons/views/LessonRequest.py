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
        # for previous_lesson in LessonRequest.objects.filter(id=request.user.id):
        #     if previous_lesson.lesson.equal_to(request):
        #         return HttpResponseBadRequest(CANNOT_BOOK_TWICE_MSG)

        # for previous_lesson in Lesson.objects.all():
        #     if previous_lesson.lesson.equal_to(request):
        #         return HttpResponseBadRequest(CANNOT_BOOK_TWICE_MSG)

        try:
            book_lesson = LessonRequestForm(request.POST)
            book_lesson = book_lesson.save()
            LessonRequest.objects.create(student_id=request.user.id, lesson_id=book_lesson.id)
        except ValueError:
            return HttpResponseBadRequest("Cannot submit incomplete form.")

        return redirect('request_lessons')
    else:
        form = LessonRequestForm()
        return render(request, 'request_lessons.html', {'lesson_form': form})
