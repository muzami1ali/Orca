'''
ContactUs contains the views to display the contact us message.

@author Muzamil Ali
@version 07/12/2022
'''
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def contact(request):
    return render(request,'contact.html')
