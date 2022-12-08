"""Orca URL Configuration

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
from lessons.views import LessonStatus, LessonRequest, AdminPanel, AccessViews, BankTransfer, Invoice, ContactUs, Home


admin.site.site_title='Music Admin'
admin.site.site_header='Music Admin'
admin.site.index_title=''
urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',Home.home,name='home'),
    path('dashboard/admin/',AdminPanel.admin_panel,name='admin_panel'),
    path('dashboard/admin/approve/<int:LessonRequestID>', AdminPanel.approve_lesson, name="approve_lesson"),
    path('dashboard/admin/delete/<int:LessonRequestID>', AdminPanel.delete_booking, name="delete_booking"),
    path('dashboard/admin/approve/payment/<int:BankTransferID>',AdminPanel.approve_bank_payment,name="approve_payment"),
    path('login/', AccessViews.log_in, name = 'login'),
    path('logout/',AccessViews.log_out, name='logout'),
    path('sign-up/',AccessViews.sign_up, name='sign-up'),
    path('booking/request/', LessonRequest.request_lessons, name='request_lessons'),
    path('booking/bank_transfer/', BankTransfer.bank_transfer, name='bank_transfer'),
    path('booking/status/', LessonStatus.request_status, name='request_status'),
    path('booking/status/edit/<int:LessonRequestID>/', LessonStatus.edit_lesson, name='edit_lesson'),
    path('booking/status/cancel/<int:LessonRequestID>/', LessonStatus.cancel_lesson, name='cancel_lesson'),
    path('booking/invoice/', Invoice.invoice, name='invoice'),
    # path('deal_requests/', Invoice.deal_requests, name='deal_requests'),
    # path('deal_requests/authorise/<int:nid>', Invoice.authorise, name='authorise'),
    # path('deal_requests/decline/<int:nid>', Invoice.decline, name='decline'),
    path('contact-us/', ContactUs.contact, name='contact-us')



]
handler404 = "lessons.views._page_not_found_view.page_not_found_view"
