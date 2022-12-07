'''
BankTransfer contains the views for the bank bank transfer webpage.

@author Muzamil Ali
@version 07/12/2022
'''
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from lessons.forms import BankTransferForm

@login_required(login_url='log_in')
def bank_transfer(request):
    if request.method == 'POST':
        form= BankTransferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_transfer')
    else:
        form = BankTransferForm()
    return render(request, 'bank_transfer.html', {'form': form})
