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

# Greeting 
@app.route("/greeting", methods=['GET'])
def greeting():
    return 'Hello world!'

# Create Employee
@app.route('/employee', methods=['POST'])
def create_employee():
    request_data = request.get_json()
    employees_data = get_employee_data()
    
    emp_id = random.randint(1,1000)
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

def sort_employees_by_name(employees_data):
    return sorted(employees_data, key=lambda x: x["name"].lower())

#search employee
@app.route('/employees/search', methods=['POST'])
def employee_search():
    request_data = request.get_json()

    # Validate the request data
    fields = request_data.get("fields")
    condition = request_data.get("condition", "AND")

    if not fields or not isinstance(fields, list) or len(fields) == 0:
        return {"messages": ["At least one search criterion should be passed."]}, 400

    errors = validate_filter_criteria(fields)
    if errors:
        return {"messages": errors}, 400

    # Load employee data from the file and sort by name
    employees_data = get_employee_data()
    employees_data = sort_employees_by_name(employees_data)

    # Perform the search using binary search
    matched_employees = []

    if condition.upper() == "AND":
        matched_employees = evaluate_filter_criteria_and_binary_search(employees_data, fields)
    elif condition.upper() == "OR":
        matched_employees = evaluate_filter_criteria_or_binary_search(employees_data, fields)

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

def evaluate_filter_criteria_and_binary_search(employees_data, fields):
    matched_employees = []

    for employee in employees_data:
        is_match = True
        for criterion in fields:
            field_name = criterion.get("fieldName")
            eq_value = criterion.get("eq")
            neq_value = criterion.get("neq")

            if field_name in employee:
                employee_value = employee[field_name].lower()  # Convert to lowercase for case-insensitive comparison
                if eq_value is not None and employee_value != eq_value.lower():
                    is_match = False
                    break
                if neq_value is not None and employee_value == neq_value.lower():
                    is_match = False
                    break
            else:
                # Field does not exist in the employee data
                is_match = False
                break

        if is_match:
            matched_employees.append(employee)

    return matched_employees

def evaluate_filter_criteria_or_binary_search(employees_data, fields):
    matched_employees = []

    for criterion in fields:
        field_name = criterion.get("fieldName")
        eq_value = criterion.get("eq")
        neq_value = criterion.get("neq")

        # Binary search based on the "name" field
        left, right = 0, len(employees_data) - 1
        while left <= right:
            mid = (left + right) // 2
            mid_name = employees_data[mid].get("name").lower()

            if eq_value is not None and mid_name == eq_value.lower():
                matched_employees.append(employees_data[mid])
                break
            elif neq_value is not None and mid_name != neq_value.lower():
                matched_employees.append(employees_data[mid])
                break
            elif mid_name < (eq_value or neq_value).lower():
                left = mid + 1
            else:
                right = mid - 1

    return matched_employees
if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0')