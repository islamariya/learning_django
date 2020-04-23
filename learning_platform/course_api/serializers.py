from rest_framework import serializers

from course.models import CourseCategory, Course, CourseFlows, Homework, CourseLecture, \
    StudentsEnrolled, StudentsHomework, CourseFlowTimetable

from my_user.models import MyUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id','category', 'title', 'is_active', 'short_description', 'overview',
                  'duration', 'price', 'version')

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer(read_only=True)
        return super(CourseSerializer, self).to_representation(instance)


class CourseFlowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFlows
        fields = ('id','course', 'start_date', 'code', 'is_over', 'curator')

    def to_representation(self, instance):
        self.fields['course'] = CourseSerializer(read_only=True)
        self.fields['curator'] = MyUserSerilizer(read_only=True)
        return super(CourseFlowsSerializer, self).to_representation(instance)


class LectureSerilizer(serializers.ModelSerializer):
    class Meta:
        model = CourseLecture
        fields = ('id', 'title', 'sequence_number', 'course', 'description', 'is_active')

    def to_representation(self, instance):
        self.fields['course'] = CourseSerializer(read_only=True)
        return super(LectureSerilizer, self).to_representation(instance)


class HomeworkSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ('id', 'title', 'sequence_number', 'course_flow', 'description',
                  'due_date', 'is_active')

    def to_representation(self, instance):
        self.fields['course_flow'] = CourseFlowsSerializer(read_only=True)
        return super(HomeworkSerilizer, self).to_representation(instance)


class MyUserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'email', 'date_of_birth',
                  'is_teacher', 'is_student', 'is_staff', 'password')

    def create(self, validated_data):
        new_user = MyUser.objects.create_user(**validated_data)
        new_user.save()
        return new_user


class StudentsenrolledSerilizer(serializers.ModelSerializer):
    class Meta:
        model = StudentsEnrolled
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['course_flow'] = CourseFlowsSerializer(read_only=True)
        self.fields['student'] = MyUserSerilizer(read_only=True)
        return super(StudentsenrolledSerilizer, self).to_representation(instance)


class StudentsHomeworkSerilizer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = StudentsHomework
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['course_flow'] = CourseFlowsSerializer(read_only=True)
        self.fields['student'] = StudentsenrolledSerilizer(read_only=True)
        self.fields['homework'] = HomeworkSerilizer(read_only=True)
        return super(StudentsHomeworkSerilizer, self).to_representation(instance)

    def get_status(self, obj):
        return obj.get_status_display()


class StudentsHomeworkSendSerilizer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = StudentsHomework
        fields = '__all__'
        read_only_fields = ('course_flow', 'student', 'homework', 'status', 'teacher_comments')

    def to_representation(self, instance):
        self.fields['course_flow'] = CourseFlowsSerializer(read_only=True)
        self.fields['student'] = StudentsenrolledSerilizer(read_only=True)
        self.fields['homework'] = HomeworkSerilizer(read_only=True)
        return super(StudentsHomeworkSendSerilizer, self).to_representation(instance)

    def get_status(self, obj):
        return obj.get_status_display()


class StudentsHomeworkCheckingSerilizer(serializers.ModelSerializer):
    class Meta:
        model = StudentsHomework
        fields = '__all__'
        read_only_fields = ('content', 'date_of_completion', 'course_flow',
                            'student', 'homework')

    def to_representation(self, instance):
        self.fields['course_flow'] = CourseFlowsSerializer(read_only=True)
        self.fields['student'] = StudentsenrolledSerilizer(read_only=True)
        self.fields['homework'] = HomeworkSerilizer(read_only=True)
        return super(StudentsHomeworkCheckingSerilizer, self).to_representation(instance)

    def get_status(self, obj):
        return obj.get_status_display()


class CourseFlowTimetableSerilizer(serializers.ModelSerializer):
    class Meta:
        model = CourseFlowTimetable
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['lesson'] = LectureSerilizer(read_only=True)
        self.fields['course_flow'] = CourseFlowsSerializer(read_only=True)
        self.fields['teacher'] = MyUserSerilizer(read_only=True)
        return super(CourseFlowTimetableSerilizer, self).to_representation(instance)
