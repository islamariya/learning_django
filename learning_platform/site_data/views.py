from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import UserCorrespondence
from .forms import ContactForm


class ContactUs(CreateView):
    model = UserCorrespondence
    form_class = ContactForm
    success_url = reverse_lazy('course:index')
    template_name = "site_data/contact.html"
