# Secure Professional Portfolio

This is a hardened Flask-based portfolio designed for a Security Engineer. It features visitor logging, secure contact form with rate limiting, and a modern "Tech AI Security" UI.

## Features
- **Hardened Backend:** Flask with SQLAlchemy (SQLite), Flask-Talisman (Security Headers), Flask-Limiter (Spam Protection), and Flask-WTF (CSRF Protection).
- **Visitor Logging:** Automatically logs IP, User-Agent, and path of all visitors.
- **Email Notifications:** Sends real-time alerts to the owner upon form submission.
- **Modern UI:** Interactive atoms/network effect using `particles.js` and a dark cybersecurity theme.

## Local Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.template` to `.env` and fill in your email credentials (use a Google App Password for Gmail).
4. Run the application:
   ```bash
   python app.py
   ```

## PythonAnywhere Deployment
1. Upload the files to your PythonAnywhere account.
2. In the **Web** tab, create a new web app using **Flask**.
3. Point the **Source code** to your project directory.
4. Set up a **Virtualenv** and install `requirements.txt`.
5. Edit the **WSGI configuration file** (found on the Web tab) and ensure it imports your `app`:
   ```python
   import sys
   path = '/home/attupatil/portfolio_project' # Update this path
   if path not in sys.path:
       sys.path.append(path)

   from app import app as application
   ```
6. Add your environment variables in the **Web** tab under "Static Files" (or use a `.env` file with `python-dotenv`).
7. **Reload** the web app.

## Security Note
This application uses a 5-minute rate limit for form submissions per IP address to prevent spam and abuse. Logs are stored in `instance/portfolio.db`.
