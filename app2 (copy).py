model = load_model('BrainTumor10Epochs.h5')
print('Model loaded. Check http://127.0.0.1:4000/')

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
            file.save(file_path)
            file_paths.append(file_path)
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
