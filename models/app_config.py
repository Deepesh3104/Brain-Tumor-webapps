# config.py
from flask import Flask

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kdeepesh702@gmail.com'  # Enter your Gmail email address
app.config['MAIL_PASSWORD'] = 'rwyi hjrz nxcw qpvd '   # Enter your Gmail password
app.config['MAIL_DEFAULT_SENDER'] = 'kdeepesh702@gmail.com'
