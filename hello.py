from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import datetime
import dns.resolver


   # Ваш остальной код

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def check_mx_record(email):
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        return False

# Создание базы данных и таблиц
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    email = request.form['textInput']

    if is_valid_email(email) and check_mx_record(email):
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is None:
            new_user = User(email=email)
            db.session.add(new_user)
            db.session.commit()
        else:
            # Логика обработки дублирующегося email
            pass

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)