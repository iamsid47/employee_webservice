from flask import Flask, request
import json
import random

app = Flask(__name__)

def save_employee_data(emp_data):
    try:
        with open("employees.json", "r") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(emp_data)

    with open("employees.json", "w") as file:
        json.dump(existing_data, file, indent=4)

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
    emp_id = rng.generate_random_number()
    
    emp_data = {
        "employeeId": str(emp_id),
        "name": request_data["name"],
        "city": request_data["city"],
    }
    save_employee_data(emp_data)
    return {"message":"Success!"}


# Get all Employee details
@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    return []

# Get Employee details
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    return {}

# Update Employee
@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    return {}

# Delete Employee
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    return {}


if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0')