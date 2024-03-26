import cv2
import numpy as np
from keras.models import load_model
from PIL import Image

model = load_model('BrainTumor10EpochsCategorical.h5')

def get_class_name(classNo):
    if classNo == 0:
        return "No Brain Tumor"
    elif classNo == 1:
        return "Yes Brain Tumor"

def get_result(img):
    image = cv2.imread(img)
    image = Image.fromarray(image, 'RGB')
    image = image.resize((64, 64))
    image = np.array(image)
    input_img = np.expand_dims(image, axis=0)
    result = np.argmax(model.predict(input_img), axis=1)
    return result
