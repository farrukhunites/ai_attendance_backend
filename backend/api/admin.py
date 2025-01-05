from django.contrib import admin
from .models import AdminLogin
from .models import ParentLogin
from .models import Student, Courses, Attendance

# Register your models here.

admin.site.register(AdminLogin)
admin.site.register(ParentLogin)
admin.site.register(Attendance)



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'first_name', 'last_name', 'email')
    list_filter = ('courses',)
    search_fields = ('roll_number', 'first_name', 'last_name', 'email')
    filter_horizontal = ('courses',)  # Allows editing ManyToMany relationships via a filter interface

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credits')
    search_fields = ('name', 'code')

