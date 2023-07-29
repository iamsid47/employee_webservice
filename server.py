from flask import Flask

app = Flask(__name__)

# Greeting 
@app.route("/greeting", methods=['GET'])
def greeting():
    return 'Hello world!'

# Create Employee
@app.route('/employee', methods=['POST'])
def create_employee():
    return {}

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