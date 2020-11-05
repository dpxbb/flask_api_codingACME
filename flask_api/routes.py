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
    gender = request.json['gender']
    address = request.json['address']
    ssn = request.json['ssn']
    email = request.json['email']

    employee = Employee(name,gender,address,ssn,email)

    db.session.add(employee)
    db.session.commit()
    results = employee_schema.dump(employee)
    return jsonify(results)

# Endpoint for All employees
@app.route('/staff', methods = ['GET'])
def get_staff():
    staff = Employee.query.all()
    return jsonify(staff_schema.dump(employee))

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