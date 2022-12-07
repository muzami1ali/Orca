'''
Home contains the views to display the home webpage.

@author
@version 07/12/2022
'''
from django.shortcuts import render

def home(request):
    return render(request,'index.html')
