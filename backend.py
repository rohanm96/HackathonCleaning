from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# In-memory storage for demonstration purposes
users = {}
reports = []
volunteers = []

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username in users:
        return jsonify({'message': 'User already exists'}), 400
    users[username] = password
    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if users.get(username) != password:
        return jsonify({'message': 'Invalid credentials'}), 400
    return jsonify({'message': 'Login successful'}), 200

@app.route('/report_issue', methods=['POST'])
def report_issue():
    data = request.form
    username = data.get('username')
    issue = data.get('issue')
    description = data.get('description')
    coordinates = data.get('coordinates')
    image = request.files['image']

    # Save the image
    image_path = os.path.join('images', f"{username}_{datetime.now().timestamp()}.jpg")
    image.save(image_path)

    report = {
        'username': username,
        'issue': issue,
        'description': description,
        'coordinates': coordinates,
        'image_path': image_path,
        'timestamp': datetime.now().isoformat()
    }
    reports.append(report)
    return jsonify({'message': 'Report submitted successfully'}), 200

@app.route('/get_reports', methods=['GET'])
def get_reports():
    return jsonify(reports), 200

@app.route('/volunteer', methods=['POST'])
def volunteer():
    data = request.json
    username = data.get('username')
    report_id = data.get('report_id')
    time_taken = data.get('time_taken')
    after_image = request.files['after_image']

    # Save the image
    after_image_path = os.path.join('images', f"after_{username}_{datetime.now().timestamp()}.jpg")
    after_image.save(after_image_path)

    volunteer_entry = {
        'username': username,
        'report_id': report_id,
        'time_taken': time_taken,
        'after_image_path': after_image_path,
        'timestamp': datetime.now().isoformat()
    }
    volunteers.append(volunteer_entry)
    return jsonify({'message': 'Volunteer report submitted successfully'}), 200

if __name__ == '__main__':
    if not os.path.exists('images'):
        os.makedirs('images')
    app.run(debug=True)
