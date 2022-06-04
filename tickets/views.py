from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View
from .forms import TicketForm
from .models import Ticket, AdminTicket


class TicketView(LoginRequiredMixin, View):
    form_class = TicketForm
    def get(self, request):
        form = self.form_class
        return render(request, 'tickets.html', {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'تیکت شما ارسال شد بزودی بررسی و نتیجه اعمال میشود پروفایل چک کنید', 'success')
        else:
            messages.error(request, 'خطا!', 'danger')
        return redirect('tickets:contactus')


class TicketPage(LoginRequiredMixin, View):
    form_class = TicketForm
    def get(self, request):
        form = self.form_class
        tickets = Ticket.objects.filter(user=request.user).order_by('-created')
        return render(request, 'tickets_page.html', {'form':form, 'tickets':tickets})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'تیکت شما ارسال شد بزودی بررسی و نتیجه اعمال میشود تیکت ها را چک کنید', 'success')
        else:
            messages.error(request, 'خطا!', 'danger')
        return redirect('tickets:tickets')

