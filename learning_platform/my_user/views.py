from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import MyUserCreationForm
from course.models import StudentsEnrolled


def login(request):
    login_form = AuthenticationForm(data=request.POST or None)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('course:index'))

    context = {
        'title': 'вход',
        'login_form': login_form,
    }

    return render(request, 'my_user/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('course:index'))


class SignUp(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('my_user:login')
    template_name = "my_user/register.html"


class Profile(generic.base.TemplateView):
    template_name = "my_user/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students_courses'] = StudentsEnrolled.objects.filter(student=self.request.user.pk)
        return context
