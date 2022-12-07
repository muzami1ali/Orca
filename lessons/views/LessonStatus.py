'''
    LessonStatus contains the views for viewing, editing, and cancelling
    requested lessons.
    @author Dean Whitbread
    @version 05/12/2022
'''
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, LessonRequest, Student
from lessons.forms import LessonRequestForm
from lessons.views import _HttpResponseConstantMsg

''' Constant Messages '''
LESSON_AUTHORISED_MSG = "Lesson has been authorised and cannot be edited."
LESSON_CANNOT_CANCEL_TWICE_MSG = "Cannot cancel the same booking twice."

@login_required
def request_status(request):
    request_status = LessonRequest.objects.filter(student=request.user)
    lesson_counter = LessonRequest.objects.filter(student=request.user).count()
    return render(request, 'request_status.html', {'request_status': request_status, 'lesson_counter': lesson_counter})


@login_required
def edit_lesson(request, LessonRequestID):
    try:
        lesson_request = LessonRequest.objects.filter(id=LessonRequestID).get()
    except LessonRequest.DoesNotExist:
        return HttpResponseBadRequest(_HttpResponseConstantMsg.DOES_NOT_EXIST_MSG)

    if request.method == 'POST':
        if lesson_request.is_authorised:
            return HttpResponseForbidden(LESSON_AUTHORISED_MSG)

        if not request.user.is_staff:
            if lesson_request.student_id != request.user.id:
                return HttpResponseForbidden(_HttpResponseConstantMsg.OTHER_USER_RECORD_MSG)

        update_lesson = Lesson.objects.filter(id=lesson_request.lesson_id).update(
            lesson_name = request.POST.get('lesson_name'),
            student_availability = request.POST.get('student_availability'),
            number_of_lessons = request.POST.get('number_of_lessons'),
            interval = request.POST.get('interval'),
            duration = request.POST.get('duration'),
            term_period = request.POST.get('term_period'),
            additional_information = request.POST.get('additional_information')
        )

        if request.user.is_staff:
            return redirect('admin_panel')
        else:
            return redirect('request_status')

    else:
        if not request.user.is_staff:
            if lesson_request.student_id != request.user.id:
                return HttpResponseForbidden(_HttpResponseConstantMsg.OTHER_USER_RECORD_MSG)

        edit_form = LessonRequestForm(
            initial={
                'lesson_name':lesson_request.lesson.lesson_name,
                'student_availability':lesson_request.lesson.student_availability,
                'number_of_lessons':lesson_request.lesson.number_of_lessons,
                'interval':lesson_request.lesson.interval,
                'duration':lesson_request.lesson.duration,
                'term_period':lesson_request.lesson.term_period,
                'additional_information':lesson_request.lesson.additional_information,
                }
            )
        return render(request, 'edit_lesson.html', {'edit_lesson_form': edit_form, 'lessonID': LessonRequestID})


@login_required
def cancel_lesson(request, LessonRequestID):
    try:
        lesson_request = LessonRequest.objects.filter(id=LessonRequestID).get(id=LessonRequestID)
    except LessonRequest.DoesNotExist:
        return HttpResponseBadRequest(_HttpResponseConstantMsg.DOES_NOT_EXIST_MSG)

    if lesson_request.is_authorised:
        return HttpResponseForbidden(LESSON_AUTHORISED_MSG)

    if request.user.is_staff:
        lesson_request.delete()
        return redirect('admin_panel')
    else:
        if lesson_request.student_id != request.user.id:
            return HttpResponseForbidden(_HttpResponseConstantMsg.OTHER_USER_RECORD_MSG)
        else:
            lesson_request.delete()
            return redirect('request_status')
