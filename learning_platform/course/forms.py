from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Course, CourseFlows, CourseLecture, Homework, CourseFlowTimetable, StudentsHomework


#Course
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        exclude = ['slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


#CourseFlows
class CourseFlowsForm(ModelForm):
    class Meta:
        model = CourseFlows
        fields = "__all__"


#Lecures
class CourseLecturesForm(ModelForm):
    class Meta:
        model = CourseLecture
        fields = "__all__"


#LecuresTimetable
class CourseLecturesForm(ModelForm):
    class Meta:
        model = CourseFlowTimetable
        fields = "__all__"


#Homework
class HomeowrkForm(ModelForm):
    class Meta:
        model = Homework
        fields = "__all__"


class StudentHomeowrkForm(ModelForm):
    class Meta:
        model = StudentsHomework
        fields = "__all__"


class StudentHomeworkSendForm(ModelForm):
    disabled_fields = ("course_flow", "student", "homework")

    class Meta:
        model = StudentsHomework
        fields = ("content","course_flow", "student", "homework")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].disabled = True


class StudentHomeworkCheckForm(ModelForm):
    disabled_fields = ("course_flow", "student", "homework", "content")

    class Meta:
        model = StudentsHomework
        fields = ("content","course_flow", "student", "homework", "teacher_comments", "status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].disabled = True