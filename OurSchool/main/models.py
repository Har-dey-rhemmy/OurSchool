from django.db import models
from django.core import serializers
import moviepy.editor

# Teeacher Model
class Teacher(models.Model):
    full_name=models.CharField(max_length=1000)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    mobile_no=models.CharField(max_length=20)
    address=models.TextField()
    otp_digit=models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name_plural="1. Teacher"
    
    def total_teacher_courses(self):
        total_courses=Course.objects.filter(teacher=self).count()
        return total_courses
    
    def total_teacher_chapter(self):
        total_chapter=Chapter.objects.filter(course_teacher=self).count()
        return total_chapter
    
    def total_teacher_chapter(self):
        total_student=StudentCourseEnroll.objects.filter(course_teacher=self).count()
        return total_student
    
    def save(self):
        if self.pk is None:
            send_mail('verify Account', 'Please, Verify your account', [self.email], fail_silently=False, html_message=f'<p>Your OTP is </p><p>{self.otp_digit}</p>')
        return super().save()

class CourseCategory(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()

    class Meta:
        verbose_name_plural="2. Course Categories"

    def __str__(self):
        return self.title

class Course(models.Model):
    category=models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_courses')
    title=models.CharField(max_length=150)
    description=models.TextField()
    featured_img=models.ImageField(upload_to='course_imgs/', null=True)
    techs=models.TextField(null=True)

    class Meta:
        verbose_name_plural="3. Courses"

    def related_videos(self):
        related_videos=Course.objects.filter(techs__icontains=self.techs)
        return serializers.serialize('json', related_videos)
    
    def __str__(self):
        return self.title

class Chapter(models.Model):
    category=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='Course_chapter')
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    description=models.TextField()
    file=models.FileField(upload_to='chapter_file/', null=True)
    remarks=models.TextField(null=True)

    class Meta:
        verbose_name_plural="4. Chapters"

class Student(models.Model):
    full_name=models.CharField(max_length=1000)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    interested_categories=models.TextField()
    otp_digit=models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.full_name

    def enrolled_courses(self):
        enrolled_courses=models.StudentCourseEnroll.objects.filter(student=self).count()
        return enrolled_courses

    class Meta:
        verbose_name_plural="5. Student"
class StudentCourseEnroll(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_course')
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrolled_student')
    enrolled=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='6. Enrolled Course'

class StudentAssignment(models.Model):
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    student=models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=200)
    detail=models.TextField(null=True)
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural='7. Assignment'