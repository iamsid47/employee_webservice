from flask import Flask, request, jsonify
import json

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
    
    emp_id = len(employees_data) + 1
    emp_data = {
        "employeeId": str(emp_id),
        "name": request_data["name"],
        "city": request_data["city"],
    }
    employees_data.append(emp_data)
    save_employee_data(employees_data)
    return {"message": "Success"}


# Get all Employee details
@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    employees_data = get_employee_data()
    return jsonify(employees_data)


# Get Employee details
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employees_data = get_employee_data()
    for employee in employees_data:
        if employee["employeeId"] == id:
            return jsonify(employee)

    return {"message": "Employee not found"}, 404

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
            return {"message": "Employee updated successfully"}
    
    return {"message": "Employee not found"}, 404

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
        last_employee = employees_data[-1]
        last_employee_id = int(last_employee["employeeId"])
        found_employee["employeeId"] = str(last_employee_id - 1)

        employees_data.remove(last_employee)

        employees_data.sort(key=lambda x: int(x["employeeId"]))

        save_employee_data(employees_data)
        return {"message": "Employee deleted successfully"}

    return {"message": "Employee not found"}, 404


if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0')