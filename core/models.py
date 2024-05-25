from django.db import (models)
import cv2
import os
import numpy as np
from PIL import Image
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import normalize, to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense


class AbstractModel(models.Model):
    updated_date = models.DateTimeField(
        blank=True,
        auto_now=True,
        verbose_name="Updated Date"
    )
    created_date = models.DateTimeField(
        blank=True,
        auto_now_add=True,
        verbose_name="Created Date"
    )

    class Meta:
        abstract = True


class Donation(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name


def preprocess_image(image_path, input_size):
    # Read image
    image = cv2.imread(image_path)
    # Convert to RGB
    image = Image.fromarray(image, 'RGB')
    # Resize image
    image = image.resize((input_size, input_size))
    # Normalize pixel values
    image_array = normalize(np.array(image), axis=1)
    # Reshape for model input
    image_array = image_array.reshape(1, input_size, input_size, 3)
    return image_array


def predict_tumor(model, input_image):
    prediction = model.predict(input_image)
    return prediction


def interpret_result(prediction):
    return "There is no brain tumor" if prediction[0][0] > prediction[0][1] else "Brain Tumor Detected"


def load_trained_model(model_path):
    try:
        # Load the pre-trained model
        model = keras.models.load_model(model_path)
        return model
    except Exception as e:
        print(f"Error loading the pre-trained model: {e}")
        return None


def calculate_threshold_percentage(results, threshold=0.5):
    flat_results = results.flatten() if len(results.shape) > 1 else results
    above_threshold_count = np.sum(flat_results >= threshold)
    total_samples = len(flat_results)
    percentage = (above_threshold_count / total_samples) * 100
    return percentage


def load_trained_model(model_path):
    try:
        model = keras.models.load_model(model_path)
        return model
    except Exception as e:
        print(f"Error loading the pre-trained model: {e}")
        return None
