from flask import Flask, request, jsonify
import nibabel as nib
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load the trained model (replace with your path to .h5 model)
model = load_model('path_to_your_model.h5')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file temporarily
    file_path = 'uploaded_image.nii'
    file.save(file_path)

    # Load and process the .nii file
    img = nib.load(file_path)
    img_data = img.get_fdata()

    # Extract the middle slice (or any other slice you want to classify)
    middle_slice = img_data[:, :, img_data.shape[2] // 2]

    # Preprocess the slice (resize, normalize, etc.)
    slice_resized = np.resize(middle_slice, (256, 256))  # Resize to match model input size
    slice_resized = slice_resized / np.max(slice_resized)  # Normalize

    # Add batch and channel dimensions
    slice_resized = np.expand_dims(slice_resized, axis=-1)  # Add channel dimension (e.g., grayscale)
    slice_resized = np.expand_dims(slice_resized, axis=0)  # Add batch dimension

    # Classify the image
    predictions = model.predict(slice_resized)

    # Get predicted class (assuming binary classification: 1 for ASD, 0 for not ASD)
    predicted_class = np.argmax(predictions, axis=1)

    if predicted_class == 1:
        result = 'The person is predicted to have ASD.'
    else:
        result = 'The person is predicted not to have ASD.'

    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)
