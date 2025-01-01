from rest_framework import serializers
from .models import AdminLogin, ParentLogin, Student, Courses

class AdminLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminLogin
        fields= ['id','username','password']

class ParentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentLogin
        fields= ['id','email','password','child_name']

# Admin Login Request Serializer
class AdminLoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100)

# Parent Login Request Serializer
class ParentLoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['id', 'name', 'code', 'credits', 'description']


class StudentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)  # Nested representation of courses

    class Meta:
        model = Student
        fields = ['id', 'roll_number', 'first_name', 'last_name', 'date_of_birth', 'email', 'parentId', 'courses']
