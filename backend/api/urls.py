from django.urls import path
from . import views
 
urlpatterns = [
    path("adminlogin/", views.AdminLoginListCreate.as_view(), name = "admin_view"),
    path("parentlogin/", views.ParentLoginListCreate.as_view(), name = "parent_view"),
    path('adminlogin/<int:pk>/', views.AdminLoginDetail.as_view(), name='admin_login_detail'),
    path('parentlogin/<int:pk>/', views.ParentLoginDetail.as_view(), name='parent_login_detail'),
    path('adminlogin/login/', views.AdminLoginView.as_view(), name='admin-login'),
    path('parentlogin/login/', views.ParentLoginView.as_view(), name='parent-login'),
    path('courses/', views.CourseListCreateView.as_view(), name='course-list-create'),
    path('students/', views.StudentListCreateView.as_view(), name='student-list-create'),
] 
