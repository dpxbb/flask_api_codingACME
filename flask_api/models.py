from flask_api import app, db, ma, login_manager
from datetime import datetime
import uuid
from flask_login import UserMixin

# Import for Werkzeug Security
from werkzeug.security import generate_password_hash, check_password_hash

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String, nullable = False)
    job = db.Column(db.String, nullable = False)
    gender = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)
    ssn = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)

    def __init__(self,full_name, job,gender,address,ssn,email,id = id):
        self.full_name = full_name
        self.job = job
        self.gender = gender
        self.address = address
        self.ssn = ssn
        self.email = email

    def __repr__(self):
        return f'Employee {self.full_name} has been added to database.'


class EmployeeSchema(ma.Schema):
    class Meta:
        # Fields to show in output
        fields = ["id", "full_name", "job", "gender","address","ssn","email"]

employee_schema = EmployeeSchema()
staff_schema = EmployeeSchema(many = True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(256), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    token = db.Column(db.String(400), default = 'No Token Created')
    token_refreshed = db.Column(db.Boolean, default = False)
    date_refreshed = db.Column(db.DateTime)

    def __init__(self,name,email,password,id = id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = self.set_password(password)

    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'{self.name} has been created successfully'