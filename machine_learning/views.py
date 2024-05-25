import os
from machine_learning.models import preprocess_image, predict_tumor, interpret_result, load_trained_model
from django.shortcuts import render
from django.http import HttpResponseBadRequest

model_path = 'C:\\Users\\ekinf\\OneDrive\\tumor\\my_site\\BrainTumorModel.h5'


def handle_uploaded_image(uploaded_file):
    # Save the uploaded file to a temporary location

    temp_file_path = 'c://path/to/' + uploaded_file.name

    with open(temp_file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return temp_file_path


def detection(request):
    if request.method == 'POST':
        # Assuming your form has a file input named 'image'
        uploaded_image = request.FILES.get('image')

        if uploaded_image:
            # Save the uploaded image to a temporary location
            image_path = handle_uploaded_image(uploaded_image)

            # Load the pre-trained model
            model = load_trained_model(model_path)

            if model:
                # Preprocess the image for prediction
                input_size = 64
                input_img = preprocess_image(image_path, input_size)

                # Make a prediction
                prediction = predict_tumor(model, input_img)

                # Interpret the result
                interpretation = interpret_result(prediction)

                # Optionally, you can remove the temporary image file here
                # os.remove(image_path)

                return render(request, 'detection_result.html', {'interpretation': interpretation})
            else:
                # Handle the case where the model fails to load
                return HttpResponseBadRequest("Error loading the pre-trained model.")

    return render(request, 'detection.html')
