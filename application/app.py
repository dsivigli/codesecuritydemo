from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import subprocess
import boto3
import hashlib
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super_insecure_secret_key"  # VULNERABILITY: Hardcoded secret key

# VULNERABILITY: Insecure database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulnerable.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# VULNERABILITY: Hardcoded AWS credentials
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "us-west-2"

# VULNERABILITY: Public S3 bucket with no access controls
S3_BUCKET = "vulnerable-demo-bucket-248189912704"  # Changed to use your account ID

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # VULNERABILITY: Passwords stored in plain text
    is_admin = db.Column(db.Boolean, default=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_private = db.Column(db.Boolean, default=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # VULNERABILITY: No password hashing
        
        # VULNERABILITY: SQL Injection in raw SQL
        # Should use parameterized queries instead
        user_exists = db.engine.execute(f"SELECT * FROM user WHERE username = '{username}'").fetchone()
        
        if user_exists:
            return "Username already exists!"
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/note/new', methods=['POST'])
def new_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    content = request.form['content']
    is_private = 'is_private' in request.form
    
    note = Note(user_id=session['user_id'], content=content, is_private=is_private)
    db.session.add(note)
    db.session.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/note/<int:note_id>')
def view_note(note_id):
    # VULNERABILITY: IDOR - no authorization check
    note = Note.query.get_or_404(note_id)
    return render_template('note.html', note=note)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # VULNERABILITY: SQL Injection
        query = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        user = db.engine.execute(query).fetchone()
        
        if user:
            session['user_id'] = user.id
            session['username'] = username
            session['is_admin'] = user.is_admin
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials!"
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # VULNERABILITY: XSS - unescaped user input
    username = session['username']
    
    # Get user notes
    notes = Note.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('dashboard.html', username=username, notes=notes)




@app.route('/execute', methods=['POST'])
def execute_command():
    # VULNERABILITY: Command injection - no authorization check and direct command execution
    if 'user_id' not in session:
        return "Unauthorized", 403
    
    # VULNERABILITY: No admin check - any logged in user can execute commands
    command = request.form.get('command', '')
    
    if not command:
        return "No command provided"
    
    try:
        # VULNERABILITY: Direct command execution without sanitization
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        output = f"Exit Code: {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return output
    except subprocess.TimeoutExpired:
        return "Command timed out after 10 seconds"
    except Exception as e:
        # VULNERABILITY: Exposing system error details
        return f"Error executing command: {str(e)}"


@app.route('/api/user/<int:user_id>')
def api_get_user(user_id):
    # VULNERABILITY: IDOR in API
    user = User.query.get_or_404(user_id)
    # VULNERABILITY: Exposing sensitive data
    return jsonify({
        'id': user.id,
        'username': user.username,
        'password': user.password,  # Exposing password!
        'is_admin': user.is_admin
    })

@app.route('/search')
def search():
    # VULNERABILITY: XSS in search parameter
    query = request.args.get('q', '')
    # Simulate search results
    results = [f"Result for: {query}"]
    return render_template('search.html', query=query, results=results)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    # VULNERABILITY: Information disclosure in error messages
    return f"Page not found: {request.path}", 404

@app.errorhandler(500)
def server_error(e):
    # VULNERABILITY: Detailed error exposure
    return f"Server error: {str(e)}", 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', password='admin123', is_admin=True)
            db.session.add(admin)
            db.session.commit()
    
    # VULNERABILITY: Debug mode enabled in production
    app.run(host='0.0.0.0', port=5001, debug=True)
