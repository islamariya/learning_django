import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, \
    UpdateView, TemplateView

from .forms import CourseFlowsForm, CourseForm, CourseLecturesForm, HomeowrkForm, \
    StudentHomeworkSendForm, StudentHomeworkCheckForm

from .models import Course, CourseFlows, CourseFlowTimetable, CourseLecture, \
    Homework, StudentsHomework


#Courses
class CoursesListView(ListView):
    model = Course
    context_object_name = "courses"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(is_active=True).order_by('-creation_date')


class CourseDetailView(DetailView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Описание курса"

        return context


class CourseCreateView(CreateView):
    model = Course
    success_url = reverse_lazy("users:profile")
    form_class = CourseForm


class CourseUpdateView(UpdateView):
    model = Course
    success_url = reverse_lazy("users:profile")
    form_class = CourseForm


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy("users:profile")

    def delete(self, request, *args, **kwargs):
        self.obj = self.get_object()
        self.obj.is_active = False
        self.obj.save()
        return HttpResponseRedirect(self.success_url)


#CourseFlows
class CoursesFlowsListView(ListView):
    model = CourseFlows
    context_object_name = "courses"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(is_active=True).order_by('start_date')


class CourseFlowsDetailView(DetailView):
    model = CourseFlows

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context["title"] = "Описание курса"

        return context


class CourseFlowsCreateView(CreateView):
    model = CourseFlows
    form_class = CourseFlowsForm
    success_url = reverse_lazy("users:profile")


class CourseFlowsUpdateView(UpdateView):
    model = CourseFlows
    form_class = CourseFlowsForm
    success_url = reverse_lazy("users:profile")


class CourseFlowsDeleteView(DeleteView):
    model = CourseFlows
    success_url = reverse_lazy("users:profile")

    def delete(self, request, *args, **kwargs):
        self.obj = self.get_object()
        self.obj.is_active = True
        self.obj.save()
        return HttpResponseRedirect(self.success_url)


#CourseLecture
class LectureListView(ListView):
    model = CourseLecture
    context_object_name = "lectures"
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs['pk']
        return self.model.objects.filter(course=pk).order_by('sequence_number')


class LectureDetailView(DetailView):
    model = CourseLecture

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Описание урока"

        return context


class LectureUpdateView(UpdateView):
    model = CourseLecture
    form_class = CourseLecturesForm
    success_url = reverse_lazy("users:profile")


class LectureDeleteView(DeleteView):
    model = CourseLecture
    success_url = reverse_lazy("users:profile")

    def delete(self, request, *args, **kwargs):
        self.obj = self.get_object()
        self.obj.is_active = False
        self.obj.save()
        return HttpResponseRedirect(self.success_url)


#CourseFlowTimetable
class FlowTimetableListView(ListView):
    model = CourseFlowTimetable
    context_object_name = "lectures"
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs['pk']
        return self.model.objects.filter(course_flow=pk).order_by('date')


class LectureTimetableDetailView(DetailView):
    model = CourseFlowTimetable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Описание урока"

        return context


class LectureTimetableUpdateView(UpdateView):
    model = CourseFlowTimetable
    form_class = CourseLecturesForm
    success_url = reverse_lazy("users:profile")


class LectureTimetableDeleteView(DeleteView):
    model = CourseFlowTimetable
    success_url = reverse_lazy("users:profile")

    def delete(self, request, *args, **kwargs):
        self.obj = self.get_object()
        self.obj.delete()
        return HttpResponseRedirect(self.success_url)


# CourseHomework
class HomeworkListView(ListView):
    model = Homework
    context_object_name = "homeworks"
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs['pk']
        return self.model.objects.filter(course_flow=pk, is_active=True)


class HomeworkDetailView(DetailView):
    model = Homework

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Описание"

        return context

class HomeworkUpdateView(UpdateView):
    model = Homework
    form_class = HomeowrkForm
    success_url = reverse_lazy("users:profile")


class HomeworkDeleteView(DeleteView):
    model = Homework
    success_url = reverse_lazy("users:profile")

    def delete(self, request, *args, **kwargs):
        self.obj = self.get_object()
        self.obj.is_active = False
        self.obj.save()
        return HttpResponseRedirect(self.success_url)


#StudentHomework
class StudentsHomeworkListView(ListView):
    model = StudentsHomework
    context_object_name = "homeworks"
    template_name = "course/studentshomework_list.html"

    def get_queryset(self):
        try:
            pk = self.kwargs["pk"]
            user = self.request.user.pk
        except KeyError:
            return self.model.objects.filter(course_flow=pk, student__student__id=user)
        queryset = {
            "student": self.model.objects.filter(course_flow=pk, student__student__id=user),
            "teacher": self.model.objects.filter(status=1)
        }
        return queryset


class StudentHomeworkDetailView(DetailView):
    model = StudentsHomework

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Описание"

        return context


class StudentHomeworkSendView(UpdateView):
    model = StudentsHomework
    form_class = StudentHomeworkSendForm
    success_url = reverse_lazy("my_user:profile")

    def get_form_class(self):
        user = self.request.user
        if user.is_teacher:
            self.form_class = StudentHomeworkCheckForm
            return self.form_class
        elif user.is_student:
            self.form_class = StudentHomeworkSendForm
            return self.form_class

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_student:
            self.object.date_of_completion = datetime.datetime.now()
            self.object.status = StudentsHomework.HOMEWORK_STATUS_ON_REVIEW
            self.object.save()
        return super().post(request, *args, **kwargs)
