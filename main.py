from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    session,
    jsonify,
    url_for,
)

#flask mail setup
from sklearn.ensemble import GradientBoostingClassifier
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score
from pymongo import MongoClient
import bcrypt
import pymongo
import warnings
import os
from motor.motor_asyncio import AsyncIOMotorClient

import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image
import cv2  # Import cv2 module
from keras.models import load_model
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image
import cv2  # Import cv2 module
from keras.models import load_model
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

from nltk_utils import bag_of_words, tokenize
from chat import get_response
import torch
import json
import random




app = Flask(__name__, static_folder='static')


# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kdeepesh702@gmail.com'  # Enter your Gmail email address
app.config['MAIL_PASSWORD'] = 'rwyi hjrz nxcw qpvd '         # Enter your Gmail password
app.config['MAIL_DEFAULT_SENDER'] = 'kdeepesh702@gmail.com'

mail = Mail(app)


# Generate a random secret key of 32 bytes (256 bits)
app.secret_key = os.urandom(24)

from motor.motor_asyncio import AsyncIOMotorClient

connection_string = "mongodb+srv://Deepesh2104:Deepesh2228@cluster0.7mgj9te.mongodb.net/deepesh?retryWrites=true&w=majority"

client = AsyncIOMotorClient(connection_string)
db = client.deepesh
users_collection = db.users

try:
    # Connect to MongoDB Atlas
    client = pymongo.MongoClient(connection_string)

    
    db = client["deepesh"]

    
    collection = db["user"] 
    # Print the fetched data

except pymongo.errors.ConnectionFailure as e:
    print("Failed to connect to MongoDB Atlas. Error:", e)




@app.route('/')
def index():
    return render_template('index.html')




# Tummor Implementations

model = load_model('BrainTumor10EpochsCategorical.h5')
print("Loading model...")

print("Model loaded successfully.")
print('Model loaded. Check http://127.0.0.1:5000/')

def get_className(classNo):
    if classNo == 0:
        return "No Brain Tumor"
    elif classNo == 1:
        return "Yes Brain Tumor"

def getResult1(img):
    image = cv2.imread(img)
    image = Image.fromarray(image, 'RGB')
    image = image.resize((64, 64))
    image = np.array(image)
    input_img = np.expand_dims(image, axis=0)
    result = np.argmax(model.predict(input_img), axis=1)
    print("Predicted class index:", result)
    print("Predicted class:", get_className(result))
    
    return result

@app.route('/tumor', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            file_path = os.path.join('static/uploads', secure_filename(f.filename))
            f.save(file_path)
            value = getResult1(file_path)
            result = get_className(value[0])
            image_url = url_for('static', filename='uploads/' + secure_filename(f.filename))
            return render_template('singleimg.html', result=result, image_url=image_url, f=f)
    return "No image uploaded!"
# Print the predicted class index


# Print the predicted class name



@app.route('/singleimg', methods=['GET'])
def singleimg():
    return render_template('singleimg.html')

# Multi Image Started



UPLOAD_FOLDER = 'static/uploads'  # Define the uploads folder
STATIC_FOLDER = 'static'   # Define the static folder

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

def get_className(classNo):
    if classNo == 0:
        return "No Brain Tumor"
    elif classNo == 1:
        return "Yes Brain Tumor"

def getResult(img_paths):
    results = []
    for img_path in img_paths:
        image = cv2.imread(img_path)
        image = Image.fromarray(image, 'RGB')
        image = image.resize((64, 64))
        image = np.array(image)
        input_img = np.expand_dims(image, axis=0)
        result = get_className(np.argmax(model.predict(input_img), axis=1)[0])
        results.append(result)
    return results

@app.route('/multiimg', methods=['GET', 'POST'])
def multiimg():
    results = []
    file_paths = []  # Initialize file_paths as an empty list
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(file_path)
                file_paths.append(file_path)
            except Exception as e:
                print("Error saving file:", e)
        results = getResult(file_paths)
    return render_template('multiimage.html', results=zip(file_paths, results))

@app.route('/tumor2', methods=['POST'])
def predict():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        file_paths = []
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_paths.append(file_path)
        results = getResult(file_paths)
        return render_template('multiimage.html', results=zip(file_paths, results))

# multi image end



# tummor Implementation end here 


# sucess alert 

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Send email
        msg = Message(subject='New message from your website',
                      sender='kdeepesh702@gmail.com',  # Your Gmail address
                      recipients=['kdeepesh702@gmail.com'])  # Your Gmail address
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)

        return render_template('success_alert.html')


    
@app.route('/sitemap.xml')
def sitemap():
    # Assuming your sitemap.xml file is located in the 'templates' directory
    return render_template('sitemap.xml')

@app.post("/predicti")
def predicti():
    try:
        text = request.get_json().get("message")
        response = get_response(text)
        message = {"answer": response}
        return jsonify(message)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login1", methods=["GET", "POST"])
def login1():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        # Find the user with the provided email in the database
        user = collection.find_one({"email": email})

        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            # Store the user's email in the session to keep them logged in
            session["user_id"] = str(user["_id"])
            return redirect(url_for("dashboard"))
        else:
            return render_template("login1.html", error="Invalid credentials")

    return render_template("login1.html")

@app.route('/logout')
def logout():
    session.pop("user_id", None)
    return render_template("index.html")

from flask import redirect, url_for

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        firstname = request.form["Firstname"]
        lastname = request.form["Lastname"]
        email = request.form["Email"]
        password = request.form["Password"]
        # Hash the password before storing it

        existing_user = collection.find_one({"email": email})
        if existing_user:
            return render_template("register.html", error="Email already exists")
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": hashed_password,
        }
        collection.insert_one(user_data)

        # Redirect to the login page after successful registration
        return redirect(url_for("login1"))

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        user_id = session["user_id"]
        user = collection.find_one({"_id": ObjectId(user_id)})
        return render_template("home.html")
    else:
        flash("Please log in first", "warning")
        return redirect(url_for("login1"))

@app.route("/services", methods=["GET", "POST"])
def services():
    return render_template("services.html")



@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contactus.html")


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

@app.route("/helpsupot", methods=["GET", "POST"])
def helpsupot():
    return render_template("help&suppot.html")



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000
    app.run(host="0.0.0.0", port=port, debug=True)
