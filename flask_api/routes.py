from flask_api import app, db
from flask_api.models import Employee, employee_schema, staff_schema, User, check_password_hash
from flask import jsonify, request, render_template, redirect, url_for
# jsonify does  it turns any of the data into a json format. very similar to a dictionary. 
# hover over jsonify to get more details 

# import for Flask Login
from flask_login import login_required, login_user, current_user, logout_user

# Import for PyJWT(Json Web Token)
import jwt

from flask_api.forms import UserForm, LoginForm

# Json is sending things the front-end. The way it comes through JavaScript is Json (JavaScript Object Notation)
# The reason we use it is so the browswer knows what is going on. So we can display it onto any front page or mobile phone. 

@app.route('/employee/create', methods = ['POST'])
def create_employee():
    name = request.json['full_name']
    job = request.json['job']
    gender = request.json['gender']
    address = request.json['address']
    ssn = request.json['ssn']
    email = request.json['email']

    employee = Employee(name,job, gender,address,ssn,email)

    db.session.add(employee)
    db.session.commit()
    results = employee_schema.dump(employee)
    return jsonify(results)

# Endpoint for All employees
@app.route('/staff', methods = ['GET'])
def get_staff():
    staff = Employee.query.all()
    return jsonify(staff_schema.dump(staff))

# Endpoint for One employee based on their ID    
@app.route('/employee/<id>', methods = ['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    results = employee_schema.dump(employee)
    return jsonify(results)

@app.route('/employee/update/<id>', methods = ['POST', 'PUT'])
def update_employee(id):
    employee = Employee.query.get(id)
    
    employee.name = request.json['full_name']
    employee.job = request.json['job']
    employee.gender = request.json['gender']
    employee.address = request.json['address']
    employee.ssn = request.json['ssn']
    employee.email = request.json['email']

    db.session.commit()

    return employee_schema.jsonify(employee)

@app.route('/employee/delete/<id>', methods = ['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(int(id))
    db.session.delete(employee)
    db.session.commit()
    result = employee_schema.dump(employee)
    return jsonify(result)
# CRUD Operations complete: Create, Retrieve, Update and Delete

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/users/register', methods = ['GET', 'POST'])
def register():
    form = UserForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User(name, email, password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', user_form = form) 
# redirect is going to find the login fucntion. render template goes to the html that it's being told. 

@app.route('/users/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    
    logged_user = User.query.filter(User.email == email).first()
    if logged_user and check_password_hash(logged_user.password, password): 
        login_user(logged_user)
        return redirect(url_for('get_key'))
    return render_template('login.html', login_form = form)
    # redirect is 301 status code. render_template is a 200 code. General sense, redirect go and get a certain html from the certain function. 

@app.route('/users/getkey', methods = ['GET'])
def get_key():
    token = jwt.encode({'public_id': current_user.id, 'email':current_user.email},app.config['SECRET_KEY'])
    user = User.query.filter_by(email = current_user.email).first()
    user.token = token 
    db.session.add(user)
    db.session.commit()
    results = token.decode('utf-8')
    return render_template('token.html', token = results)

# Get a new API Key
@app.route('/users/updatekey', methods = ['GET', 'POST', 'PUT'])
def refresh_key():
    refresh_key = {'refreshToken': jwt.encode({'public_id':current_user.id, 'email': current_user.email}, app.config['SECRET_KEY'])}
    temp = refresh_key.get('refreshToken')
    new_token = temp.decode('utf-8')

    # Adding Refreshed Token to DB
    user = User.query.filter_by(email = current_user.email).first()
    user.token = new_token

    db.session.add(user)
    db.session.commit()
    
    return render_template('token_refresh.html', new_token = new_token)