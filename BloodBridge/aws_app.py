from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import boto3
import uuid
import os
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

app = Flask(__name__)
app.secret_key = 'bloodbridge_secret_key'  # Change this for production

# AWS Configuration
REGION = 'us-east-1' 

# Initialize AWS Resources
# Note: AWS Credentials are not hardcoded. They will be picked up from the Environment or IAM Role.
dynamodb = boto3.resource('dynamodb', region_name=REGION)
sns = boto3.client('sns', region_name=REGION)

# DynamoDB Tables Configuration
TABLE_USERS = 'BloodBridge_Users'
TABLE_REQUESTS = 'BloodBridge_Requests'
TABLE_INVENTORY = 'BloodBridge_Inventory'

users_table = dynamodb.Table(TABLE_USERS)
requests_table = dynamodb.Table(TABLE_REQUESTS)
inventory_table = dynamodb.Table(TABLE_INVENTORY)

# SNS Topic ARN Configuration
# This should be set in the EC2 Setup or Environment Variable. 
# Providing a placeholder/example ARN as per instructions to not hardcode sensitive info, 
# or assuming it is provided via env var 'SNS_TOPIC_ARN'.
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:123456789012:BloodBridgeAlerts')

def send_notification(subject, message):
    """Sends an SNS notification."""
    if not SNS_TOPIC_ARN:
        print("SNS Topic ARN not configured.")
        return

    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
        print(f"SNS Notification sent: {subject}")
    except ClientError as e:
        print(f"Error sending SNS notification: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if not (name and email and password and role):
            flash('All fields are required!', 'danger')
            return redirect(url_for('signup'))

        # Check if user already exists
        try:
            response = users_table.get_item(Key={'email': email})
            if 'Item' in response:
                flash('Email already registered!', 'danger')
                return redirect(url_for('signup'))
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
            flash('System error during registration.', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = {
            'email': email, # PK
            'user_id': str(uuid.uuid4()),
            'name': name,
            'password': hashed_password,
            'role': role
        }
        
        try:
            users_table.put_item(Item=new_user)
            print(f"User Registered (DynamoDB): {email}")
            
            # Optional: Notify admin or self about signup? 
            # send_notification("New User Signup", f"User {name} ({role}) has signed up.")
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
            flash('Error creating account.', 'danger')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            response = users_table.get_item(Key={'email': email})
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
            flash('Login service currently unavailable.', 'danger')
            return render_template('login.html')

        user = response.get('Item')

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['user_name'] = user['name']
            session['role'] = user['role']
            session['email'] = user['email']
            
            # send_notification("User Login", f"User {user['name']} has logged in.")
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    role = session['role']
    
    requests_data = []
    inventory_data = []

    try:
        # Fetch Requests
        # Ideally we would query based on status or user, but for now we Scan all
        req_res = requests_table.scan()
        requests_data = req_res.get('Items', [])
        # Sort manually by timestamp if possible
        requests_data.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        # Fetch Inventory
        inv_res = inventory_table.scan()
        inventory_data = inv_res.get('Items', [])
        
    except ClientError as e:
        print(f"DynamoDB Error: {e}")
        flash('Error loading dashboard data.', 'warning')

    return render_template('dashboard.html', 
                           user=session, 
                           requests=requests_data, 
                           inventory=inventory_data)

@app.route('/request_blood', methods=['GET', 'POST'])
def request_blood():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        blood_type = request.form.get('blood_type')
        quantity = request.form.get('quantity')
        urgency = request.form.get('urgency')

        if not (blood_type and quantity and urgency):
            flash('All fields are required', 'danger')
            return redirect(url_for('request_blood'))

        request_id = str(uuid.uuid4())
        
        new_request = {
            'request_id': request_id, # PK
            'blood_type': blood_type,
            'quantity': int(quantity),
            'urgency': urgency,
            'requested_by': session['user_name'],
            'requester_role': session['role'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'Pending'
        }
        
        try:
            requests_table.put_item(Item=new_request)
            print(f"New Blood Request (DynamoDB): {new_request}")
            
            # EMERGENCY: Send SNS Notification
            if urgency in ['High', 'Critical']:
                send_notification(
                    f"EMERGENCY: {urgency} Blood Request",
                    f"Urgent Request Details:\n\nType: {blood_type}\nQuantity: {quantity} units\nHospital/User: {session['user_name']}\nUrgency: {urgency}\nTime: {new_request['timestamp']}"
                )
                
            flash('Blood request submitted successfully!', 'success')
            return redirect(url_for('dashboard'))
            
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
            flash('Error submitting request.', 'danger')

    return render_template('request_blood.html')

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    can_edit = session['role'] == 'blood_bank'

    if request.method == 'POST':
        if not can_edit:
            flash('Unauthorized action.', 'danger')
            return redirect(url_for('inventory'))
            
        blood_type = request.form.get('blood_type')
        quantity = int(request.form.get('quantity'))
        action = request.form.get('action') # add or remove

        try:
            # Get current item
            response = inventory_table.get_item(Key={'blood_type': blood_type})
            item = response.get('Item')
            
            current_qty = 0
            if item:
                current_qty = int(item['quantity'])
            
            new_qty = current_qty
            
            if action == 'add':
                new_qty += quantity
                msg_type = 'success'
                msg = f'Added {quantity} unit(s) of {blood_type}.'
            elif action == 'remove':
                if current_qty >= quantity:
                    new_qty -= quantity
                    msg_type = 'warning'
                    msg = f'Removed {quantity} unit(s) of {blood_type}.'
                else:
                    flash('Insufficient stock!', 'danger')
                    return redirect(url_for('inventory'))
            
            # Update Item
            inventory_table.put_item(Item={
                'blood_type': blood_type, # PK
                'quantity': new_qty,
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            flash(msg, msg_type)
            
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
            flash('Error updating inventory.', 'danger')

        return redirect(url_for('inventory'))

    try:
        response = inventory_table.scan()
        inventory_list = response.get('Items', [])
    except ClientError:
        inventory_list = []
        
    return render_template('inventory.html', inventory=inventory_list, can_edit=can_edit)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    # Ensure this runs on all interfaces for EC2 access
    app.run(debug=True, host='0.0.0.0', port=5000)
