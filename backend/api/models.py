from django.db import models

# Models
class AdminLogin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)  # Store hashed passwords
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class ParentLogin(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store hashed passwords
    child_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Courses(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)  # Course code (e.g., CS101)
    credits = models.IntegerField(default=2)
    semester = models.IntegerField(default=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    parentId = models.ForeignKey(
        ParentLogin,
        on_delete=models.CASCADE,
        related_name='children'
    )
    courses = models.ManyToManyField(Courses, related_name='students')  # Many-to-Many relationship

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"
    

class Attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey('Courses', on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status_choices = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('early_left', 'Early Left'),
    ]
    status = models.CharField(max_length=20, choices=status_choices)

    def __str__(self):
        return f"{self.student.first_name} - {self.course.name} on {self.date} - {self.status}"
