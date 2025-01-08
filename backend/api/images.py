from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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

            # Optionally clean up temporary files after processing
            default_storage.delete(file_path)

        return JsonResponse({
            "message": "Images received successfully.",
            "images": images,
        }, status=200)

    return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)
