from rest_framework import serializers
from . import models

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Teacher
        fields=['id', 'full_name', 'email', 'password', 'qualification', 'otp_digit', 'mobile_no', 'address', 'teacher_courses', 'total_teacher_courses']
        
    def __init__(self, *args, **kwargs):
        super(TeacherSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 1


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CourseCategory
        fields=['id', 'title', 'description']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Course
        fields=['id', 'category', 'teacher', 'title', 'description', 'featured_img', 'techs', 'Course_chapter', 'related_videos']
        depth=1

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Chapter
        fields=['id', 'title', 'description', 'file', 'remarks']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Student
        fields=['id', 'full_name', 'email', 'password', 'interested_categories']
        depth=1

    

class StudentCourseEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.StudentCourseEnroll
        fields=['id', 'Course', 'Student', 'enrolled']

class StudentAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.StudentAssignment
        fields=['id', 'teacher', 'student', 'title', 'detail', 'add_time']
    
    def __init__(self, *args, **kwargs):
        super(CourseSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2