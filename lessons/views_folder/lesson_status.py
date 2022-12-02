'''
    View for the 'Lesson Status' page.
    @author Dean Whitbread
    @version 02/12/2022
'''
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, LessonRequest
from lessons.forms import LessonRequestForm


@login_required(login_url='/log_in/')
def request_status(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            request_status = LessonRequest.objects.filter(student=request.user)
            lesson_counter = LessonRequest.objects.filter(student=request.user).count()
            return render(request, 'request_status.html', {'request_status': request_status, 'lesson_counter': lesson_counter})
    else:
        return redirect('log_in')


@login_required(login_url='/log_in/')
def edit_lesson(request, LessonRequestID):
    if request.method == 'POST':
        try:
            if request.user.id == LessonRequest.objects.get(id=LessonRequestID).student_id:
                lesson_request = LessonRequest.objects.filter(id=LessonRequestID).get()
                booked_lesson = Lesson.objects.filter(id=lesson_request.lesson_id).update(
                    lesson_name = request.POST.get('lesson_name'),
                    student_availability = request.POST.get('student_availability'),
                    number_of_lessons = request.POST.get('number_of_lessons'),
                    interval = request.POST.get('interval'),
                    duration = request.POST.get('duration'),
                    term_period = request.POST.get('term_period'),
                    additional_information = request.POST.get('additional_information')
                )
            else:
                return HttpResponseForbidden("Cannot edit other student lesson requests")
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Lesson request does not exist.")
        except MultipleObjectsReturned:
            return HttpResponseBadRequest("Multiple lesson objects found.")

        return redirect('request_status')
    else:
        if LessonRequest.objects.filter(id=LessonRequestID).exists():
            if request.user.id == LessonRequest.objects.get(id=LessonRequestID).student_id:
                lesson_request = LessonRequest.objects.get(id=LessonRequestID)
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
            else:
                return HttpResponseForbidden("Cannot edit other student lesson requests")
        else:
            return HttpResponseForbidden("Cannot edit this lesson request.")
    return render(request, 'edit_lesson.html', {'edit_lesson_form': edit_form, 'lessonID': LessonRequestID})


@login_required(login_url='/log_in/')
def cancel_lesson(request, LessonRequestID):
    if request.method == 'POST':
        lesson_request_object = LessonRequest.objects.filter(id=LessonRequestID)
        if lesson_request_object.exists():
            if (LessonRequest.objects.get(id=LessonRequestID)).student_id == request.user.id:
                try:
                    LessonRequest.objects.get(id=LessonRequestID).delete()
                except IntegrityError:
                    pass
            else:
                return HttpResponseForbidden("Cannot cancel lesson booked by another student.")
        else:
            return HttpResponseBadRequest("Cannot cancel the same booking twice.")
    return redirect('request_status')
