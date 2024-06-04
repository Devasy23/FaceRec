from __future__ import annotations

import base64
import json
import os

import requests
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request

from FaceRec.config import Config

flk_blueprint = Blueprint(
    'flk_blueprint ',
    __name__,
    template_folder='../../templates/',
    static_folder='../../static/',
)


@flk_blueprint.route('/')
def Main_page():
    path = str(Config.upload_image_path[0])
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    else:
        pass
    return redirect('DisplayingEmployees')


# Displaying all records
@flk_blueprint.route('/DisplayingEmployees')
def display_information():
    global employees
    url = 'http://127.0.0.1:8000/Data/'
    try:
        resp = requests.get(url=url)
        # logger.info(resp.status_code)
        # logger.info(resp.json())
        employees = resp.json()

    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    return render_template('table.html', employees=employees)


# To add employee record
@flk_blueprint.route('/Add_employee')
def add_employee():
    return render_template('index.html')


# To submit the form data to server and save it in database
@flk_blueprint.route('/submit_form', methods=['POST'])
def submit_form():

    Employee_Code = request.form['EmployeeCode']
    Name = request.form['Name']
    gender = request.form['Gender']
    Department = request.form['Department']

    if request.files['File']:
        if 'File' not in request.files:
            return jsonify({'message': 'No file part'}), 400
        file = request.files['File']
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if (
            '.' not in file.filename
            or file.filename.split('.')[-1].lower() not in allowed_extensions
        ):
            return jsonify({'message': 'File extension is not valid'}), 400
        if file:
            image_data = file.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            with open(Config.image_data_file, 'w') as file:
                json.dump({'base64_image': encoded_image}, file)

    with open(Config.image_data_file) as file:
        image_data = json.load(file)
    encoded_image = image_data.get('base64_image', '')
    jsonify(
        {
            'EmployeeCode': Employee_Code,
            'Name': Name,
            'gender': gender,
            'Department': Department,
            'encoded_image': encoded_image,
        },
    )

    payload = {
        'EmployeeCode': Employee_Code,
        'Name': Name,
        'gender': gender,
        'Department': Department,
        'Image': encoded_image,
    }
    url = 'http://127.0.0.1:8000/create_new_faceEntry'
    try:
        resp = requests.post(
            url=url,
            json={
                'EmployeeCode': 134,
                'Name': 'Name',
                'gender': 'gender',
                'Department': 'Department',
                'Image': 'your_image',
            },
        )
        resp.status_code
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    jsonify({'message': 'Successfully executed'})
    print('Executed.')
    if resp.status_code == 200:
        return redirect('DisplayingEmployees')
    else:
        return jsonify({'message': 'Failed to execute'})


# To edit an employee details
@flk_blueprint.route('/edit/<int:EmployeeCode>', methods=['POST', 'GET'])
def edit(EmployeeCode):
    if request.method == 'POST':
        Name = request.form['Name']
        gender = request.form['Gender']
        Department = request.form['Department']
        with open(Config.image_data_file) as file:
            image_data = json.load(file)
        encoded_image = image_data.get('base64_image', '')
        payload = {
            'Name': Name,
            'gender': gender,
            'Department': Department,
            'Image': encoded_image,
        }
        # logger.info(payload)
        try:
            url = requests.put(
                f'http://127.0.0.1:8000/update/{EmployeeCode}', json=payload,
            )
            url.status_code
            # logger.info(url.json())

            return redirect('/')

        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')
    response = requests.get(f'http://127.0.0.1:8000/read/{EmployeeCode}')
    # logger.info(response.status_code)
    # logger.info(response.json())
    if response.status_code == 200:
        employee_data = response.json()
        return render_template('edit.html', employee_data=employee_data)
    else:
        return f'Error {response.status_code}: Failed to retrieve employee data.'


# To delete employee details
@flk_blueprint.route('/Delete/<int:EmployeeCode>', methods=['DELETE', 'GET'])
def Delete(EmployeeCode):
    if not isinstance(EmployeeCode, int):
        return jsonify({'message': 'Employee code should be an integer'}, 400)
    response = requests.delete(f'http://127.0.0.1:8000/delete/{EmployeeCode}')
    jsonify(response.json())

    return redirect('/DisplayingEmployees')
