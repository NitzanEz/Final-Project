import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

def classify_images(image_folder, model_path):
    model = load_model(model_path)
    images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpeg')]
    results = []
    for image_path in images:
        img = load_img(image_path, color_mode='rgb', target_size=(128, 128))
        img_array = img_to_array(img)
        img_array /= 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)
        confidence = np.max(prediction)
        results.append((image_path, predicted_class[0], confidence))
        print(f"Processed {image_path}: Class {predicted_class[0]}, Confidence {confidence:.2f}")
    return results



image_directory = 'C:/Users/liorb/Downloads/GUI/GUI/backend/patients/KKI/KKI/0050772'
model_file_path = 'model.h5'
predictions = classify_images(image_directory, model_file_path)
