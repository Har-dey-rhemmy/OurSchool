import random
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import TeacherSerializer, CategorySerializer, CourseSerializer, ChapterSerializer, StudentSerializer, StudentCourseEnrollSerializer, StudentAssignmentSerializer
from . import models

class TeacherList(generics.ListCreateAPIView):
    queryset=models.Teacher.objects.all()
    serializer_class=TeacherSerializer
    #permission_classes=[permissions.IsAuthenticated]

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Teacher.objects.all()
    serializer_class=TeacherSerializer
    #permission_classes=[permissions.IsAuthenticated]

@csrf_exempt
def teacher_login(request):
    email=request.POST('email')
    password=request.POST('password')
    try:
        teacherData=models.Teacher.objects.get(email=email, password=password)
    except models.Teacher.DoesNotExist:
        teacherData=None

    if teacherData:
        if not teacherData.verify_status:
            return JsonResponse({'bool':False, 'teacher_id': teacherData.id, 'msg': 'Account is not verified!'})
        else:
            return JsonResponse({'bool':True, 'teacher_id': teacherData.id})
    else:
        return JsonResponse({'bool':False, 'msg': 'Invalid Email or Password!!'})
    
def verify_teacher(request, teacher_id):
    otp_digit=request.POST.get['otp digit']
    verify=models.Teacher.objects.filter(id=teacher_id, otp_digit=otp_digit).update(status=True)
    if verify:
        return JsonResponse({'bool': True, 'teacher_id': verify.id})
    else:
        return JsonResponse({'bool': False})
    
class CategoryList(generics.ListCreateAPIView):
    queryset=models.CourseCategory.objects.all()
    serializer_class=CategorySerializer

class CourseList(generics.ListCreateAPIView):
    queryset=models.Course.objects.all()
    serializer_class=CourseSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        if 'result' in self.request.GET:
            limit=int(self.request.GET['result'])
            qs=models.Course.objects.all().order_by('_id')[:limit]
            return qs

class TeacherCourseList(generics.ListAPIView):
    serializer_class=CourseSerializer

    def get_queryset(self):
        teacher_id=self.kwargs('teacher_id')
        teacher=models.Teacher.objects.get(pk=teacher_id)
        return models.Course.objects.filter(teacher=teacher)

class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Course.objects.all()
    serializer_class=CourseSerializer

class ChapterList(generics.ListCreateAPIView):
    queryset=models.Chapter.objects.all()
    serializer_class=ChapterSerializer

    def get_queryset(self):
        course_id=self.kwargs('course_id')
        course=models.Course.objects.get(pk=course_id)
        return models.Chapter.objects.filter(course=course)
    
class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Chapter.objects.all()
    serializer_class=ChapterSerializer

class CourseDetailView(generics.RetrieveAPIView):
    queryset=models.Course.objects.all()
    serializer_class=CourseSerializer

class StudentList(generics.ListCreateAPIView):
    queryset=models.Student.objects.all()
    serializer_class=StudentSerializer
    #permission_classes=[permissions.IsAuthenticated]

@csrf_exempt
def student_login(request):
    email=request.POST('email')
    password=request.POST('password')
    try:
        studentData=models.Student.objects.get(email=email, password=password)
    except models.Student.DoesNotExist:
        studentData=None

    if studentData:
        return JsonResponse({'bool':True, 'student_id': studentData.id})
    else:
        return JsonResponse({'bool':False})

def verify_student(request, student_id):
    otp_digit=request.POST.get('otp_digit')
    verify=models.Student.objects.filter(id=student_id, otp_digit=otp_digit).update(verify_status=True)
    if verify:
        return JsonResponse({'bool': True, 'student_id': verify.id})
    else:
        return JsonResponse({'bool': False})

class StudentEnrollCourseList(generics.ListCreateAPIView):
    queryset=models.StudentCourseEnroll.objects.all()
    serializer_class=StudentCourseEnrollSerializer

def fetch_enroll_status(request, student_id, course_id):
    student=models.StudentCourseEnroll.objects.filter(id=student_id)
    course=models.Course.objects.filter(id=course_id).first()
    serializer_class=StudentCourseEnrollSerializer
    enrollStatus=models.StudentCourseEnroll.objects.filter(course=course, student=student).count()

    if enrollStatus:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})
    
class AssignmentList(generics.ListCreateAPIView):
    queryset=models.StudentAssignment.objects.all()
    serializer_class=StudentAssignmentSerializer

    def get_queryset(self):
        student_id=self.kwargs['student_id']
        teacher_id=self.kwargs['teacher_id']
        student=models.Student.objects.get(pk=student_id)
        teacher=models.Teacher.objects.get(pk=teacher_id)
        return models.StudentAssignment.objects.filter(student=student, teacher=teacher)
    
@csrf_exempt
def teacher_forgot_password(request, teacher_id):
    email=request.POST.get('email')
    verify=models.Teacher.objects.filter(id=teacher_id, email=email).first()
    if verify:
        otp_digit= random.randint(100000, 999999)
        link=f'http://localhost:3000/teacher-change-password/{verify_id}'
        models.Teacher.objects.filter(email=email).update(otp_digit=otp_digit)
        return JsonResponse({'bool': True, 'teacher_id': verify.id})
    else:
        return JsonResponse({'bool': False, 'msg': 'Invalid Email!'})