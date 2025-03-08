from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from datetime import datetime
from markupsafe import Markup
import markdown2
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pythonmaster.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Association table for user badges
user_badges = db.Table('user_badges',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('badge_id', db.Integer, db.ForeignKey('badge.id'), primary_key=True),
    db.Column('earned_date', db.DateTime, default=db.func.current_timestamp())
)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    xp_points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    badges = db.relationship('Badge', secondary='user_badges')

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    image_url = db.Column(db.String(200))

class PythonLesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20))
    xp_reward = db.Column(db.Integer, default=10)

class LinuxLesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20))
    xp_reward = db.Column(db.Integer, default=10)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.template_filter('markdown')
def markdown_filter(text):
    return Markup(markdown2.markdown(text))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/python-lessons')
@login_required
def python_lessons():
    section = request.args.get('section', 'basics')
    query = PythonLesson.query
    if section == 'strings':
        query = query.filter(PythonLesson.title.like('%String%'))
    elif section == 'numbers':
        query = query.filter(PythonLesson.title.like('%Number%'))
    lessons = query.all()
    return render_template('python_lessons.html', lessons=lessons, current_section=section)

@app.route('/execute-code', methods=['POST'])
@login_required
def execute_code():
    code = request.json.get('code')
    if not code:
        return jsonify({'error': 'No code provided'})
    
    try:
        # Create a string buffer to capture output
        import io
        import sys
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        
        # Execute the code
        exec(code)
        
        # Get the output
        output = output_buffer.getvalue()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        sys.stdout = sys.__stdout__

@app.route('/linux-lessons')
@login_required
def linux_lessons():
    lessons = LinuxLesson.query.all()
    return render_template('linux_lessons.html', lessons=lessons)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
            
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
