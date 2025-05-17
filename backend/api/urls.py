from django.urls import path
from . import views
from .images import receive_images
 
urlpatterns = [
    path("adminlogin/", views.AdminLoginListCreate.as_view(), name = "admin_view"),
    path("parentlogin/", views.ParentLoginListCreate.as_view(), name = "parent_view"),
    path('adminlogin/<int:pk>/', views.AdminLoginDetail.as_view(), name='admin_login_detail'),
    path('parentlogin/<int:pk>/', views.ParentLoginDetail.as_view(), name='parent_login_detail'),
    path('adminlogin/login/', views.AdminLoginView.as_view(), name='admin-login'),
    path('parentlogin/login/', views.ParentLoginView.as_view(), name='parent-login'),
    path('courses/', views.CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/student/<int:student_id>/', views.CoursesByStudentView.as_view(), name='courses-by-student'),


    path('students/', views.StudentListCreateView.as_view(), name='student-list-create'),
    path('student/<int:student_id>/', views.StudentDetailView.as_view(), name='student-detail'),

    # Mark attendance for a specific student and course
    path('attendance/mark/', views.MarkAttendanceView.as_view(), name='mark-attendance'),
    path('attendance/<int:attendance_id>/', views.DeleteAttendanceView.as_view(), name='delete-attendance'),


    # Retrieve attendance for a specific student and course
    path('attendance/<int:course_id>/<int:student_id>/', views.MarkAttendanceView.as_view(), name='get-student-course-attendance'),
    path('receive-images/', receive_images, name='receive_images'),

] 
