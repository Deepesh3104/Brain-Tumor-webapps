import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from models import app_config, database_handling, mail_handling, routes
from models.model_utils import get_result, get_class_name

from flask import Flask
from models import app_config
from models.routes import register_routes

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        file_path = os.path.join('uploads', secure_filename(f.filename))
        f.save(file_path)
        value = get_result(file_path)
        result = get_class_name(value[0])
        return result
    return "No image uploaded!"


# Load app configurations
app.config.from_object(app_config)

# Register routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
