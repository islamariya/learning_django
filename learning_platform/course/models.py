from django.db import models
from django.utils.text import slugify

from my_user.models import MyUser


class CourseCategory(models.Model):
    """This models represents Course Categories, showing in main menu (like Programming, Marketing, DevOps, etc)"""
    title = models.CharField(max_length=70, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Слег')
    is_active = models.BooleanField(default=False, verbose_name='Активная категория')

    class Meta:
        verbose_name = 'Категори'
        verbose_name_plural = 'Категории'
        ordering = ["title"]

    def __str__(self):
        return self.title


class Course(models.Model):
    """This models represents information about Courses. Unactive course is not shown at the web-site but can be used
    to get some statistic data in reports.
    Each course has a version (integer: 1,2,3, etc) Please add a new version in case of serious modifications of
    course (like price changing).
    Course duration is a sting in format: "4 месяца, 4 академ. часа в неделю Пн 20:00, Чт 20:00".
    Each launch of course in represented in class CourseFlows. """
    title = models.CharField(max_length=70, blank=False, verbose_name='Наименование курса')
    slug = models.SlugField(max_length=200, verbose_name='Слег')
    is_active = models.BooleanField(default=False, verbose_name='Курс доступен')
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='categories',
                                 verbose_name='Категория')
    short_description = models.CharField(max_length=300, verbose_name='Краткое описание')
    overview = models.TextField(verbose_name='Описание')
    duration = models.CharField(max_length=100, verbose_name='Продолжительность')
    price = models.IntegerField(verbose_name='Цена')
    creation_date = models.DateField(auto_now_add=True)
    version = models.IntegerField(verbose_name='Версия курса')


    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title']

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} версия {self.version}'


class CourseLecture(models.Model):
    """This class represents Lectures, that should be given in course. This models contains general information
    about lecture such as title, sequence_number in study plan, info (description, goals, etc), version.
    Each lecture should be attached to specific version of course.
    Specific data like tutor, date will be provided in CourseFlowTimetable."""
    title = models.CharField(max_length=100, blank=False, verbose_name='Тема занятия')
    sequence_number = models.IntegerField(verbose_name='Порядковый Номер занятия в курсе')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='syllabus',
                               verbose_name='Курс')
    description = models.TextField(verbose_name='Описание занятия')
    is_active = models.BooleanField(verbose_name='Доступность', default=False)
    version = models.IntegerField(verbose_name='Версия урока', default=1)

    class Meta:
        verbose_name = 'Учебный план курса'
        verbose_name_plural = 'Учебные планы курсов'
        ordering = ['title']

    def __str__(self):
        return f'"{self.title}" курса "{self.course}"'


class CourseFlows(models.Model):
    """This class represents each launch of course. Course code is should have a abbreviation of course subject and
    start date (like, PHP 10.2019) """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_flows', verbose_name='Курс')
    start_date = models.DateField(blank=False, verbose_name='Дата начала')
    curator = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='course_flows',
                                verbose_name='Куратор')
    code = models.CharField(max_length=50, unique=True, verbose_name='Код потока')
    is_over = models.BooleanField(default=False, verbose_name='Поток завершен')

    class Meta:
        verbose_name = 'Поток (набор) курса'
        verbose_name_plural = 'Потоки курсов'
        ordering = ['start_date']

    def __str__(self):
        return f'{self.course} {self.start_date}'

    def __repr__(self):
        return f'{self.course} {self.start_date}'


class Homework(models.Model):
    """This class represents homework, that should be done during each course flow. """
    title = models.CharField(verbose_name='Название', max_length=200, blank=False)
    sequence_number = models.IntegerField(verbose_name='Порядковый номер в курсе', default=1)
    course_flow = models.ForeignKey(CourseFlows, on_delete=models.CASCADE, related_name='homework',
                                    verbose_name='Поток курса')
    description = models.TextField(verbose_name='Описание')
    due_date = models.DateField(verbose_name='Срок сдачи')
    is_active = models.BooleanField(verbose_name='Доступность', default=False)

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'

    def __str__(self):
        return f'№{self.sequence_number} {self.title} {self.course_flow}'


class StudentsEnrolled(models.Model):
    """This class represents Students enrolled in each Course Flow"""
    course_flow = models.ForeignKey(CourseFlows, on_delete=models.CASCADE, related_name='students_in_flow',
                                    verbose_name='Поток курса')
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='students_in_flow',
                                verbose_name='Студент')
    start_learning_date = models.DateField(verbose_name='Дата начала обучения')
    is_active = models.BooleanField(default=True, verbose_name='Учится')

    class Meta:
        verbose_name = 'Студенты в потоке'
        verbose_name_plural = 'Студенты в потоке'

    def __str__(self):
        return f'{self.student} {self.course_flow}'


class StudentsHomework(models.Model):
    """This course represents information about each Student's academic performance.  """
    HOMEWORK_STATUS_NOT_DONE = 0
    HOMEWORK_STATUS_ON_REVIEW = 1
    HOMEWORK_STATUS_SEND_TO_REWORK = 2
    HOMEWORK_STATUS_COMPLETE = 3
    HOMEWORK_STATUS_CHOICES = ((HOMEWORK_STATUS_NOT_DONE, "Не сдано"),
                               (HOMEWORK_STATUS_ON_REVIEW, "На проверке"),
                               (HOMEWORK_STATUS_SEND_TO_REWORK, "Отправлено на доработку"),
                               (HOMEWORK_STATUS_COMPLETE, "Сдано")
                               )


    course_flow = models.ForeignKey(CourseFlows, on_delete=models.CASCADE, related_name='students_homework',
                                    verbose_name='Поток курса')
    student = models.ForeignKey(StudentsEnrolled, on_delete=models.CASCADE, related_name='students_homework',
                                verbose_name='Студент')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='students_homework',
                                 verbose_name='Дом задание')
    date_of_completion = models.DateField(blank=True, null=True, verbose_name='Факт дата сдачи')
    content = models.TextField(max_length=300, default='Прикрепите ссылку на репозиторий',
                               blank=True, verbose_name='Содержание')
    status = models.PositiveSmallIntegerField(choices=HOMEWORK_STATUS_CHOICES, default=HOMEWORK_STATUS_NOT_DONE,
                                              verbose_name='Статус работы')
    teacher_comments = models.TextField(blank=True, verbose_name='Комментарии преподавателя')

    class Meta:
        verbose_name = 'Успеваемость студентов'
        verbose_name_plural = 'Успеваемость студентов'

    def __str__(self):
        return f'Домашняя работа "{self.homework.title}" Student {self.student.student.first_name}'


class CourseFlowTimetable(models.Model):
    """This class represents timetable of each Course Flow."""
    lesson = models.ForeignKey(CourseLecture, on_delete=models.CASCADE, related_name='courseflow_timetable',
                               verbose_name='Номер занятия')
    course_flow = models.ForeignKey(CourseFlows, on_delete=models.CASCADE, related_name='courseflow_timetable',
                                    verbose_name='Поток курса')
    date = models.DateTimeField(verbose_name='Дата занятия')
    teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Преподаватель')

    class Meta:
        verbose_name = 'Расписание занятий'
        verbose_name_plural = 'Расписание занятий'

    def __str__(self):
        return f"{self.lesson} {self.date}"
