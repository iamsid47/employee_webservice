import json
from flask import Flask, request

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

if __name__ == "__main__":
    app.run()
