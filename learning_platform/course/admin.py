from django.contrib import admin

from .models import CourseCategory, Course, CourseLecture, Homework, CourseFlows, StudentsHomework, \
                     CourseFlowTimetable, StudentsEnrolled


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_active', 'version']
    ordering = ('category', 'title', '-version')
    prepopulated_fields = {'slug':('title',)}
    search_fields = ('title', 'category')
    list_filter = ['category', 'is_active']
    save_as = True


@admin.register(CourseLecture)
class CourseLectureAdmin(admin.ModelAdmin):
    list_display = ['course', 'sequence_number', 'title']
    list_display_links = ('sequence_number', 'title')
    ordering = ('course', 'sequence_number')
    list_filter = ['course', 'course__version', 'sequence_number']
    save_as = True


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title','sequence_number', 'course_flow']
    list_filter = ['course_flow']
    ordering = ('course_flow', 'sequence_number')
    date_hierarchy = 'due_date'
    save_as = True


@admin.register(CourseFlows)
class CourseFlowsAdmin(admin.ModelAdmin):
    list_display = ['course', 'code', 'start_date', 'is_active']
    list_filter = ['course__category', 'course', 'is_active']
    ordering = ('course', '-start_date')
    date_hierarchy = 'start_date'
    search_fields = ('course',)
    save_as = True


@admin.register(StudentsEnrolled)
class StudentsEnrolledAdmin(admin.ModelAdmin):
    list_display = ['student', 'is_active']
    # 'course_code'
    list_filter = ['course_flow__course__category', 'course_flow__course', 'course_flow',
                   ('student', admin.RelatedOnlyFieldListFilter), 'is_active']
    search_fields = ('student',)
    save_as = True


@admin.register(StudentsHomework)
class StudentsHomeworkAdmin(admin.ModelAdmin):
    list_display = ['student', 'homework', 'status']
    list_display_links = ['student', 'homework']
    list_filter = ['course_flow__course', 'course_flow', 'student', 'homework', 'status']
    search_fields = ['student', 'homework']
    save_as = True


@admin.register(CourseFlowTimetable)
class CourseFlowTimetableAdmin(admin.ModelAdmin):
    list_display = ['course_flow', 'lesson', 'date']
    list_filter = ['course_flow', 'lesson']
    save_as = True
