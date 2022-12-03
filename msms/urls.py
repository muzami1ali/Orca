"""msms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from lessons import views
from lessons.views_folder import lesson_status, lesson_request


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('log_in/', views.log_in, name = 'log_in'),
    path('log_out/',views.log_out, name='log_out'),
    path('sign_up/',views.sign_up, name='sign_up'),
    path('booking/',views.booking, name='booking'),
    path('booking/request/', lesson_request.request_lessons, name='request_lessons'),
    path('booking/bank_transfer/', views.bank_transfer, name='bank_transfer'),
    path('booking/status/', lesson_status.request_status, name='request_status'),
    path('booking/status/edit/<int:LessonRequestID>/', lesson_status.edit_lesson, name='edit_lesson'),
    path('booking/status/cancel/<int:LessonRequestID>/', lesson_status.cancel_lesson, name='cancel_lesson'),
    path('invoice/', views.invoice, name='invoice'),
    path('contact/', views.contact, name='contact')
]
