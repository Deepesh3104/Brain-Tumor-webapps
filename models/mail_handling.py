# mailhandling.py

from flask import Flask, render_template, request, redirect, flash, session, jsonify, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Enter your Gmail email address
app.config['MAIL_PASSWORD'] = 'your_password'         # Enter your Gmail password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)

@app.route("/send_email", methods=['POST'])
def send_email():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Send email
        msg = Message(subject='New message from your website',
                      sender='your_email@gmail.com',  # Your Gmail address
                      recipients=['your_email@gmail.com'])  # Your Gmail address
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)

        return redirect(url_for('success_alert'))

@app.route('/success_alert')
def success_alert():
    return render_template('success_alert.html')

if __name__ == "__main__":
    app.run(debug=True)
