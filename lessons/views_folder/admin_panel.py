from django_tables2 import MultiTableMixin
from django.views.generic.base import TemplateView
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from lessons.models import Lesson, LessonRequest, Student, Invoice, InvoiceNumber
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class AdminTableView(ListView,LoginRequiredMixin):
 pass