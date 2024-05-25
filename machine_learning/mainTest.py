import cv2
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np


def preprocess_image(image_path, input_size):
    image = cv2.imread(image_path)
    image = Image.fromarray(image)
    image = image.resize((input_size, input_size))
    image_array = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    expanded_image = np.expand_dims(image_array, axis=0)
    return expanded_image


def predict_tumor(model, image_path, input_size):
    input_img = preprocess_image(image_path, input_size)
    result = model.predict(input_img)
    return result


def interpret_result(result, threshold=0.5):
    # Assuming binary classification
    if result[0, 0] >= threshold:
        return 'No tumor detected.'
    else:
        return 'Tumor Detected'


if __name__ == "__main__":
    model = load_model('BrainTumorModel.h5', compile=True)
    image_path = 'C:\\Users\\ekinf\\OneDrive\\brain_tumor_project\\pred\\pred0.jpg'
    input_size = 64
    prediction = predict_tumor(model, image_path, input_size)
    interpretation = interpret_result(prediction)

    print(interpretation)


def calculate_threshold_percentage(results, threshold=0.5):
    """
    Calculate the percentage of samples above the given threshold.

    Parameters:
    - results: 1D or 2D array or tensor containing model outputs.
    - threshold: Threshold for classification (default is 0.5).

    Returns:
    - percentage: Percentage of samples above the threshold.
    """
    # Flatten the results if it's a 2D array or tensor
    flat_results = results.flatten() if len(results.shape) > 1 else results

    # Count the number of samples above the threshold
    above_threshold_count = np.sum(flat_results >= threshold)

    # Calculate the percentage
    total_samples = len(flat_results)
    percentage = (above_threshold_count / total_samples) * 100

    return percentage


# Example usage:
import numpy as np

# Assuming 'outputs' is an array or tensor containing model results
outputs = np.array([0.7, 0.4, 0.6, 0.8, 0.2])

# Using the default threshold of 0.5
threshold_percentage = calculate_threshold_percentage(outputs)

print(f"Percentage of samples above the threshold: {threshold_percentage:.2f}%")

