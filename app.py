import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from models import db, ContactMessage, VisitorLog

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
csrf = CSRFProtect(app)

# Security Headers
csp = {
    'default-src': [
        '\'self\'',
        'https://cdnjs.cloudflare.com',
        'https://fonts.googleapis.com',
        'https://fonts.gstatic.com'
    ],
    'script-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'https://cdnjs.cloudflare.com'
    ],
    'style-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'https://fonts.googleapis.com',
        'https://cdnjs.cloudflare.com'
    ]
}
Talisman(app, content_security_policy=csp)

# Rate Limiting: 5-minute buffer for form submissions
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

@app.before_request
def log_visitor():
    if request.endpoint and 'static' not in request.endpoint:
        log = VisitorLog(
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            path=request.path
        )
        db.session.add(log)
        db.session.commit()

def send_email_notification(name, email, subject, message):
    mail_server = os.getenv('MAIL_SERVER')
    mail_port = int(os.getenv('MAIL_PORT', 587))
    mail_username = os.getenv('MAIL_USERNAME')
    mail_password = os.getenv('MAIL_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    if not all([mail_server, mail_username, mail_password, receiver_email]):
        print("DEBUG: Email configuration missing in .env")
        return

    msg_content = f"New message from {name} ({email}):\n\nSubject: {subject}\n\nMessage:\n{message}"
    msg = MIMEText(msg_content)
    msg['Subject'] = f"PORTFOLIO ALERT: {subject}"
    msg['From'] = mail_username
    msg['To'] = receiver_email

    try:
        print(f"DEBUG: Attempting to send email via {mail_server}...")
        server = smtplib.SMTP(mail_server, mail_port)
        server.set_debuglevel(1)
        server.starttls()
        server.login(mail_username, mail_password)
        server.send_message(msg)
        server.quit()
        print("DEBUG: Email sent successfully!")
    except Exception as e:
        print(f"DEBUG: Failed to send email: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
@limiter.limit("1 per 5 minutes", methods=["POST"])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not all([name, email, subject, message]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('contact'))

        new_message = ContactMessage(name=name, email=email, subject=subject, message=message)
        db.session.add(new_message)
        db.session.commit()

        send_email_notification(name, email, subject, message)
        flash('Thank you for your message! I will get back to you soon.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
