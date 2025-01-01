from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from .models import AdminLogin, ParentLogin, Student, Courses
from .serializers import AdminLoginSerializer, ParentLoginSerializer, AdminLoginRequestSerializer,ParentLoginRequestSerializer, StudentSerializer
from .serializers import CourseSerializer
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

