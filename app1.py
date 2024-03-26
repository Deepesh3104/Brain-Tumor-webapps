import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image
import cv2
from keras.models import load_model
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
model = load_model('BrainTumor10Epochs.h5')
print('Model loaded. Check http://127.0.0.1:5000/')

def get_className(classNo):
    if classNo == 0:
        return "No Brain Tumor"
    elif classNo == 1:
        return "Yes Brain Tumor"

def detect_tumor(image):
    # Implement simple edge detection algorithm as a placeholder for object detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges

def getResult(img_paths):
    results = []
    for img_path in img_paths:
        image = cv2.imread(img_path)
        image_copy = image.copy()
        image = Image.fromarray(image, 'RGB')
        image = image.resize((64, 64))
        image = np.array(image)
        input_img = np.expand_dims(image, axis=0)
        result = get_className(np.argmax(model.predict(input_img), axis=1)[0])
        
        detected_tumor_image = detect_tumor(image_copy)
        
        results.append((result, detected_tumor_image))
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        basepath = os.path.dirname(__file__)
        file_paths = []
        for file in files:
            file_path = os.path.join(basepath, 'uploads', secure_filename(file.filename))
            file.save(file_path)
            file_paths.append(file_path)
        results = getResult(file_paths)
        return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
