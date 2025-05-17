from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import date
from .models import Attendance, Student, Courses  # Assuming you have models for Student and Courses
import subprocess
import os
import ast

students = [
    {"id": 10, "name": "Aahad"},
    {"id": 11, "name": "Fahad"},
    {"id": 12, "name": "GUjjar"},
    {"id": 13, "name": "Daud"},
    {"id": 14, "name": "Zunaira"},
    {"id": 15, "name": "Sameed"},
    {"id": 16, "name": "Ali"},
    {"id": 17, "name": "Saqib"},
    {"id": 18, "name": "Baba"},
    {"id": 19, "name": "Bisma"},
    {"id": 20, "name": "Damysha"},
    {"id": 21, "name": "Unaiza"},
]

def predict_images(image_path):
    # Adjust the path to your executable
    ai_model_executable = os.path.join(os.path.dirname(__file__), "dist", "ai_model")

    # Run the executable with the image path as an argument
    try:
        result = subprocess.run(
            [ai_model_executable, image_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            check=True,
        )
        # Process and return the output from the executable
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Handle errors from the executable
        print(f"Error executing ai_model: {e.stderr}")
        return None


@csrf_exempt
def receive_images(request):
    if request.method == 'POST':

        course_id = request.POST.get('courseId', None)

        if not course_id:
            return JsonResponse({"error": "courseId is required."}, status=400)

        if len(request.FILES) != 3:
            return JsonResponse({"error": "Exactly 3 images are required."}, status=400)

        images = {}
        today = date.today()

        # Get the course object (assuming it exists in the database)
        try:
            course = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            return JsonResponse({"error": "Course does not exist."}, status=400)

        all_students_in_course = course.students.all()  # All students enrolled in the course
        present_students = set()  # To track students marked as 'present'
        late_students = set()  # To track students marked as 'late'

        for i, (key, image_file) in enumerate(request.FILES.items(), start=1):
            # Save the image temporarily
            file_path = default_storage.save(f"temp_image_{image_file.name}", ContentFile(image_file.read()))
            images[f"image_{i}_name"] = image_file.name
            images[f"image_{i}_size"] = image_file.size
            images[f"image_{i}_type"] = image_file.content_type

            # Use the modified predict_images function
            prediction = predict_images(file_path)

            start_index = prediction.rfind("[")  # Find the last opening bracket
            end_index = prediction.rfind("]")   # Find the last closing bracket

            if start_index != -1 and end_index != -1:
                array_string = prediction[start_index:end_index + 1]
                last_array = ast.literal_eval(array_string)  # Safely evaluate the string representation
            else:
                last_array = []

            images[f"image_{i}_prediction"] = last_array

            # Iterate over students based on the image prediction
            if i == 1:  # First Image: Mark present and absent
                for student_name in last_array:
                    # Check if the student is enrolled in the course
                    student = next((student for student in students if student["name"] == student_name), None)
                    if student and student["id"] in [s.id for s in all_students_in_course]:
                        # Mark present for this student
                        Attendance.objects.update_or_create(
                            student_id=student["id"],
                            course=course,
                            date=today,
                            defaults={'status': 'present'}
                        )
                        present_students.add(student["id"])

                # Mark all other enrolled students as absent
                for student in all_students_in_course:
                    if student.id not in present_students:
                        Attendance.objects.update_or_create(
                            student=student,
                            course=course,
                            date=today,
                            defaults={'status': 'absent'}
                        )

            elif i == 2:  # Second Image: Mark late for new students
                for student_name in last_array:
                    student = next((student for student in students if student["name"] == student_name), None)
                    if student and student["id"] in [s.id for s in all_students_in_course]:
                         if student["id"] not in present_students and student["id"] not in late_students:
                            # Change absent to late for students not marked present in the first image
                            Attendance.objects.update_or_create(
                                student_id=student["id"],
                                course=course,
                                date=today,
                                defaults={'status': 'late'}
                            )
                            late_students.add(student["id"])

            elif i == 3:  # Third Image: Mark early left for students who left
                for student_id in present_students:  # Only consider students marked as 'present'
                # Check if the student is not detected in the third picture
                    if student_id not in [s["id"] for s in students if s["name"] in last_array]:
            # Update attendance status to 'early_left'
                        Attendance.objects.update_or_create(
                        student_id=student_id,
                        course=course,
                        date=today,
                        defaults={'status': 'early_left'}
                        )

            # Optionally clean up temporary files after processing
            default_storage.delete(file_path)

        return JsonResponse({
            "message": "Images received successfully and attendance marked.",
            "images": images,
        }, status=200)

    return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)
