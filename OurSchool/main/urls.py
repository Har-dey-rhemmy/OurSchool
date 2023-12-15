from django.urls import path
from . import views

urlpatterns = [
    path('teacher/', views.TeacherList.as_view()),
    path('teacher/<int:pk>/', views.TeacherDetail.as_view()),
    path('teacher-login', views.teacher_login),
    path('category/', views.CategoryList.as_view()),
    path('course/<int:pk>', views.CourseList.as_view()),
    path('course-chapters/<int:course_id', views.ChapterList.as_view()),
    path('chapter/<int:pk>', views.ChapterDetailView.as_view()),
    path('teachercourses/<int:teacher_id>', views.TeacherCourseList.as_view()),
    path('teachercourses--detail/<int:course_id>', views.TeacherCourseDetail.as_view()),
    path('student/', views.StudentList.as_view()),
    path('student-login', views.student_login),
    path('student-enroll-course/', views.StudentEnrollCourseList.as_view()),
    path('fetch-enroll-status/<int:student_id>/<int:course_id>', views.fetch_enroll_status),
]