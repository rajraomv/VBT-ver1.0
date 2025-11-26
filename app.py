from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import sys
from datetime import datetime
from functools import wraps
from storage import load_library, get_book, save_library
from manage import add_book_logic, refresh_book_logic, delete_book_logic
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
print(f"DEBUG: MONGO_URI is set: {'MONGO_URI' in os.environ}")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_view'))
        else:
            error = 'Invalid password'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('landing_view'))

@app.route('/')
def landing_view():
    return render_template('landing.html')

@app.route('/library')
def library_view():
    library = load_library()
    return render_template('library.html', books=library['books'])

@app.route('/admin')
@login_required
def admin_view():
    library = load_library()
    
    # Load recent contact messages
    messages = []
    
    # Try MongoDB first
    if os.environ.get('MONGO_URI'):
        try:
            from database import mongo_get_all_feedback
            messages = mongo_get_all_feedback()
        except Exception as e:
            print(f"Error fetching feedback from MongoDB: {e}")
            
    # If no messages from MongoDB (or not connected), try local files
    if not messages:
        log_dir = 'email_logs'
        if os.path.exists(log_dir):
            log_files = sorted(
                [f for f in os.listdir(log_dir) if f.startswith('email_') and f.endswith('.txt')],
                reverse=True
            )[:10]  # Get 10 most recent
            
            for filename in log_files:
                try:
                    with open(os.path.join(log_dir, filename), 'r') as f:
                        content = f.read()
                        messages.append({
                            'filename': filename,
                            'content': content,
                            'timestamp': filename.replace('email_', '').replace('.txt', '')
                        })
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
    
    return render_template('admin.html', books=library['books'], messages=messages)

@app.route('/book/<book_id>')
def book_view(book_id):
    book = get_book(book_id)
    if not book:
        return "Book not found", 404
    return render_template('book.html', book=book)

@app.route('/api/progress', methods=['POST'])
def update_progress():
    data = request.json
    book_id = data.get('book_id')
    chapter_id = data.get('chapter_id')
    completed = data.get('completed', False)
    
    if not book_id or not chapter_id:
        return jsonify({"status": "error", "message": "Missing book_id or chapter_id"}), 400

    library = load_library()
    book_found = False
    
    for book in library['books']:
        if book['id'] == book_id:
            book_found = True
            chapter_found = False
            for chapter in book['chapters']:
                if chapter['id'] == chapter_id:
                    chapter_found = True
                    chapter['completed'] = completed
                    break
            
            if not chapter_found:
                return jsonify({"status": "error", "message": "Chapter not found"}), 404
            
            # Recalculate total book progress
            total_chapters = len(book['chapters'])
            completed_chapters = sum(1 for c in book['chapters'] if c.get('completed'))
            book['total_progress'] = (completed_chapters / total_chapters) * 100 if total_chapters > 0 else 0
            break
    
    if not book_found:
        return jsonify({"status": "error", "message": "Book not found"}), 404

    save_library(library)
    return jsonify({"status": "success", "progress": book.get('total_progress', 0)})

@app.route('/api/admin/add_book', methods=['POST'])
@login_required
def api_add_book():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"status": "error", "message": "URL is required"}), 400
    
    # Pass None for title to let logic fetch it
    result = add_book_logic(url, None)
    return jsonify(result)

@app.route('/api/admin/delete_book/<book_id>', methods=['DELETE'])
@login_required
def api_delete_book(book_id):
    result = delete_book_logic(book_id)
    return jsonify(result)

@app.route('/api/admin/refresh_all', methods=['POST'])
@login_required
def api_refresh_all():
    library = load_library()
    results = []
    for book in library['books']:
        res = refresh_book_logic(book['id'])
        results.append(f"{book['title']}: {res['message']}")
    
    return jsonify({"status": "success", "message": "Refreshed all books."})

@app.route('/contact')
def contact_view():
    return render_template('contact.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    whatsapp = request.form.get('whatsapp')
    feedback = request.form.get('feedback')

    if not name or not email or not feedback:
        flash('Please fill in all required fields.', 'error')
        return redirect(url_for('contact_view'))

    # Prepare email content
    subject = f"New Contact Form Submission from {name}"
    body = f"""
    Name: {name}
    Email: {email}
    Phone: {phone or 'N/A'}
    WhatsApp: {whatsapp or 'N/A'}
    
    Feedback:
    {feedback}
    """
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 1. Save to MongoDB (if available)
    if os.environ.get('MONGO_URI'):
        try:
            from database import mongo_save_feedback
            feedback_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'whatsapp': whatsapp,
                'feedback': feedback,
                'timestamp': timestamp
            }
            mongo_save_feedback(feedback_data)
            print("Saved feedback to MongoDB.")
        except Exception as e:
            print(f"Error saving to MongoDB: {e}")

    # 2. Always log to console (visible in Render logs)
    print("="*50, file=sys.stderr)
    print("NEW CONTACT FORM SUBMISSION", file=sys.stderr)
    print(f"Date: {timestamp}", file=sys.stderr)
    print(f"Name: {name}", file=sys.stderr)
    print(f"Email: {email}", file=sys.stderr)
    print(f"Phone: {phone or 'N/A'}", file=sys.stderr)
    print(f"WhatsApp: {whatsapp or 'N/A'}", file=sys.stderr)
    print(f"Feedback:\n{feedback}", file=sys.stderr)
    print("="*50, file=sys.stderr)
    
    # 3. Also save to log file (for local development backup)
    log_dir = 'email_logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"email_{file_timestamp}.txt"
    filepath = os.path.join(log_dir, filename)
    
    try:
        with open(filepath, 'w') as f:
            f.write(f"Date: {timestamp}\n")
            f.write(body + "\n")
    except Exception as e:
        print(f"Error saving log file: {e}", file=sys.stderr)

    # 4. Attempt to send email
    if send_email(subject, body):
        flash('Your message has been sent successfully!', 'success')
    else:
        flash(f'Message saved to database/logs. (Email not configured)', 'success')

    return redirect(url_for('contact_view'))

def send_email(subject, body):
    sender_email = os.environ.get('MAIL_USERNAME')
    receiver_email = "tellitaudio@gmail.com"
    password = os.environ.get('MAIL_PASSWORD')
    smtp_server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('MAIL_PORT', 587))

    if not sender_email or not password:
        print("Email configuration missing.")
        return False

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
