from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)

EMPLOYEES_FILE = "employees.json"

def save_employee_data(data):
    with open(EMPLOYEES_FILE, "w") as file:
        json.dump(data, file, indent=4)

def get_employee_data():
    try:
        with open(EMPLOYEES_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

class RandomNumberGenerator:
    def __init__(self):
        self.numbers = list(range(1, 1001))
        random.shuffle(self.numbers)

    def generate_random_number(self):
        if not self.numbers:
            self.numbers = list(range(1, 1001))
            random.shuffle(self.numbers)

        return self.numbers.pop()
rng = RandomNumberGenerator()

# Greeting 
@app.route("/greeting", methods=['GET'])
def greeting():
    return 'Hello world!'

# Create Employee
@app.route('/employee', methods=['POST'])
def create_employee():
    request_data = request.get_json()
    employees_data = get_employee_data()
    
    emp_id = rng.generate_random_number()
    emp_data = {
        "employeeId": str(emp_id),
        "name": request_data["name"],
        "city": request_data["city"],
    }
    employees_data.append(emp_data)
    save_employee_data(employees_data)
    return {"employeeId": str(emp_id)}, 201


# Get all Employee details
@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    employees_data = get_employee_data()
    return jsonify(employees_data), 200


# Get Employee details
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employees_data = get_employee_data()
    for employee in employees_data:
        if employee["employeeId"] == id:
            return jsonify(employee), 200

    return {"message": f"Employee with {id} was not found"}, 404

# Update Employee
@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    request_data = request.get_json()
    employees_data = get_employee_data()

    for employee in employees_data:
        if employee["employeeId"] == id:
            employee["name"] = request_data["name"]
            employee["city"] = request_data["city"]
            save_employee_data(employees_data)
            return jsonify(employee), 201
    
    return {"message": f"Employee with {id} was not found"}, 404

# Delete Employee
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employees_data = get_employee_data()
    found_employee = None

    for employee in employees_data:
        if employee["employeeId"] == id:
            found_employee = employee
            break

    if found_employee:
        employees_data.remove(found_employee)
        save_employee_data(employees_data)
        return jsonify(found_employee), 200

    return {"message": f"Employee with {id} was not found"}, 404

#search employee
@app.route("/employee/search", methods=["POST"])
def employee_search():
    request_data = request.get_json()
    fields = request_data.get("fields")
    condition = request_data.get("condition", "AND")

    if not fields or not isinstance(fields, list) or len(fields) == 0:
        return {"message": "At least one search criteria should be passed."}, 400

    errors = validate_filter_criteria(fields)
    if errors:
        return {"messages": errors}, 400

    employees_data = get_employee_data()
    matched_employees = []

    for employee in employees_data:
        is_match = evaluate_filter_criteria(employee, fields, condition)
        if is_match:
            matched_employees.append(employee)

    return jsonify(matched_employees)

def validate_filter_criteria(fields):
    errors = []
    for criterion in fields:
        field_name = criterion.get("fieldName")
        if not field_name:
            errors.append("fieldName must be set.")

        eq_value = criterion.get("eq")
        neq_value = criterion.get("neq")
        if eq_value is None and neq_value is None:
            errors.append(f"{field_name}: At least one of eq, neq must be set.")
        elif eq_value is not None and neq_value is not None:
            errors.append(f"{field_name}: Only one of eq, neq should be set, not both.")

    return errors

def evaluate_filter_criteria(employee, fields, condition):
    for criterion in fields:
        field_name = criterion.get("fieldName")
        eq_value = criterion.get("eq")
        neq_value = criterion.get("neq")

        if field_name in employee:
            if eq_value is not None and employee[field_name] != eq_value:
                return False
            if neq_value is not None and employee[field_name] == neq_value:
                return False
        else:
            # Field does not exist in the employee data
            return False

    return True if condition == "OR" else False

if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0')