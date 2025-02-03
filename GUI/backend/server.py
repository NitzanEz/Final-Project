from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
import nibabel as nib
import tensorflow as tf
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from werkzeug.utils import secure_filename  # Correctly import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "http://localhost:3000"}})  # Adjust origins as needed

UPLOAD_FOLDER = 'C:/Users/liorb/Downloads/GUI/GUI/backend'
MODEL_PATH = 'model.h5'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = load_model(MODEL_PATH)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not file.filename.endswith('.nii'):
        return jsonify({'error': 'Invalid file type, expected .nii file'}), 400

    # Create a unique folder for this upload
    patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], os.path.splitext(file.filename)[0])
    os.makedirs(patient_folder, exist_ok=True)

    filename = secure_filename(file.filename)  # Use secure_filename to sanitize the file name
    file_path = os.path.join(patient_folder, filename)
    file.save(file_path)

    try:
        results, diagnosis = classify_file(file_path, patient_folder)

        # מציאת התוצאה עם הקונפידנס הגבוה ביותר בטווח (0, 0.95)
        best_result = max(
            [r for r in results if 0.0 < r['confidence'] < 0.95], 
            key=lambda x: x['confidence'], 
            default=None
        )

        response = {
            'message': 'File uploaded and classified successfully',
            'filename': filename,
            'best_result': best_result,  # ציון הקונפידנס הגבוה ביותר בטווח (0,0.95)
            'diagnosis': diagnosis
        }
    except Exception as e:
        response = {'error': 'Failed to process and classify file', 'message': str(e)}
    finally:
        # Clean up: Remove all extracted images and delete the patient folder
        for img_file in os.listdir(patient_folder):
            os.remove(os.path.join(patient_folder, img_file))
        os.rmdir(patient_folder)

    return jsonify(response)

def classify_file(file_path, output_folder):
    img = nib.load(file_path)
    img_data = img.get_fdata()
    
    # Export slices as images
    for i in range(img_data.shape[2]):  # Iterate over all slices
        slice_img = img_data[:, :, i]
        slice_img = (slice_img / np.max(slice_img) * 255).astype(np.uint8) if np.max(slice_img) > 0 else slice_img
        slice_img_resized = cv2.resize(slice_img, (128, 128))  # Resize to match model input
        img_filename = os.path.join(output_folder, f'slice_{i}.jpeg')
        cv2.imwrite(img_filename, slice_img_resized)  # Save as .jpeg

    # Perform classification on extracted images
    results = classify_images(output_folder, MODEL_PATH)

    # התעלמות מתוצאות עם קונפידנס של 0 או מעל 0.95 לפני חישוב האבחון
    filtered_results = [r for r in results if 0.0 < r['confidence'] < 0.95]
    
    # Determine diagnosis based on majority voting
    autism_count = sum(1 for item in filtered_results if item['predicted_class'] == 0)  # Class 0 is ASD
    non_autism_count = sum(1 for item in filtered_results if item['predicted_class'] == 1)  # Class 1 is non-ASD

    # אם כל התוצאות נפסלו (כלומר, כל הקונפידנסים היו מחוץ לטווח), נקבע שאין מספיק מידע
    if len(filtered_results) == 0:
        diagnosis = "Insufficient confidence data"
    else:
        diagnosis = "Autism Detected" if autism_count > non_autism_count else "No Autism Detected"

    return results, diagnosis

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

        # מציאת הקונפידנס הגבוה ביותר בטווח (0,0.95)
        valid_confidences = prediction[(prediction > 0.0) & (prediction < 0.95)]
        confidence = np.max(valid_confidences) if valid_confidences.size > 0 else 0.0

        predicted_class = np.argmax(prediction, axis=1)[0]  # Extract predicted class

        # Convert NumPy types to native Python types
        results.append({
            'image_path': image_path,
            'predicted_class': int(predicted_class),  # Convert int64 → int
            'confidence': round(float(confidence), 4)  # להחזיר קונפידנס עם 2 ספרות אחרי הנקודה
        })

        print(f"Processed {image_path}: Class {int(predicted_class)}, Confidence {round(float(confidence), 2):.2f}")

    return results

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
