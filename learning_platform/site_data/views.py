from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy

from .models import UserCorrespondence
from .forms import ContactForm
from .tasks import send_email, send_email_admin


class ContactUs(CreateView):
    model = UserCorrespondence
    form_class = ContactForm
    success_url = reverse_lazy('course:index')
    template_name = 'site_data/contact.html'

    def form_valid(self, form):
        if form.is_valid:
            email = form.cleaned_data.get("email")
            name = form.cleaned_data.get("name")
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
        send_email.delay(email, name, subject, message)
        send_email_admin.delay(email, name, subject, message)
        return super(ContactUs, self).form_valid(form)
