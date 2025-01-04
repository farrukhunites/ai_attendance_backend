from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Attendance, AdminLogin, ParentLogin, Student, Courses
from .serializers import AdminLoginSerializer, ParentLoginSerializer, AdminLoginRequestSerializer,ParentLoginRequestSerializer, StudentSerializer
from .serializers import CourseSerializer
from .serializers import AttendanceSerializer
# Create your views here.

class AdminLoginListCreate(generics.ListCreateAPIView):
    queryset = AdminLogin.objects.all()
    serializer_class = AdminLoginSerializer
    
class ParentLoginListCreate(generics.ListCreateAPIView):
    queryset = ParentLogin.objects.all()
    serializer_class = ParentLoginSerializer

# Course Views
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer

# Student Views
class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        return StudentSerializer

class AdminLoginDetail(generics.RetrieveAPIView):
    queryset = AdminLogin.objects.all()
    serializer_class = AdminLoginSerializer

    def get(self, request, pk):
        admin = get_object_or_404(AdminLogin, id=pk)
        serializer = self.serializer_class(admin)
        return Response(serializer.data)

# Retrieve a single Parent by ID
class ParentLoginDetail(generics.RetrieveAPIView):
    queryset = ParentLogin.objects.all()
    serializer_class = ParentLoginSerializer

    def get(self, request, pk):
        parent = get_object_or_404(ParentLogin, id=pk)
        serializer = self.serializer_class(parent)
        return Response(serializer.data)
    
    # Admin Login View
class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginRequestSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Validate username and password
            admin = AdminLogin.objects.filter(username=username, password=password).first()
            if admin:
                admin_serializer = AdminLoginSerializer(admin)
                return Response(
                    {"message": "Login successful", "admin": admin_serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Parent Login View
class ParentLoginView(APIView):
    def post(self, request):
        serializer = ParentLoginRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Validate email and password
            parent = ParentLogin.objects.filter(email=email, password=password).first()
            if parent:
                parent_serializer = ParentLoginSerializer(parent)
                return Response(
                    {"message": "Login successful", "parent": parent_serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Attendance Views
class MarkAttendanceView(APIView):
    def post(self, request):
        """
        Marks attendance for a given student and course.
        """
        data = request.data
        student_id = data.get('student_id')
        course_id = data.get('course_id')
        date = data.get('date')
        status_value = data.get('status')

        if not all([student_id, course_id, date, status_value]):
            return Response({"error": "All fields (student_id, course_id, date, status) are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(id=student_id)
            course = Courses.objects.get(id=course_id)
        except (Student.DoesNotExist, Courses.DoesNotExist):
            return Response({"error": "Invalid student_id or course_id."}, status=status.HTTP_404_NOT_FOUND)

        attendance, created = Attendance.objects.get_or_create(
            student=student,
            course=course,
            date=date,
            defaults={'status': status_value}
        )

        if not created:
            return Response({"error": "Attendance for this student, course, and date already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, course_id, student_id):
        """
        Retrieves attendance records for a specific student and course.
        """
        try:
            course = Courses.objects.get(id=course_id)
            student = Student.objects.get(id=student_id)
        except (Courses.DoesNotExist, Student.DoesNotExist):
            return Response({"error": "Invalid course_id or student_id."}, status=status.HTTP_404_NOT_FOUND)

        attendance_records = Attendance.objects.filter(course=course, student=student)
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)
