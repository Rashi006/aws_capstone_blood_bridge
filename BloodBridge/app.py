from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'bloodbridge_secret_key'  # Change this for production

# In-memory data structures
users = []
blood_requests = []
blood_inventory = []

# Dummy Data for testing
blood_inventory.append({'blood_type': 'A+', 'quantity': 10, 'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
blood_inventory.append({'blood_type': 'O-', 'quantity': 5, 'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

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
        for user in users:
            if user['email'] == email:
                flash('Email already registered!', 'danger')
                return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = {
            'id': len(users) + 1,
            'name': name,
            'email': email,
            'password': hashed_password,
            'role': role
        }
        users.append(new_user)
        print(f"User Registered: {new_user}") # Log to terminal
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = next((u for u in users if u['email'] == email), None)

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role']
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
    # Filter requests or data based on role if needed
    
    return render_template('dashboard.html', 
                           user=session, 
                           requests=blood_requests, 
                           inventory=blood_inventory)

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

        new_request = {
            'id': len(blood_requests) + 1,
            'blood_type': blood_type,
            'quantity': int(quantity),
            'urgency': urgency,
            'requested_by': session['user_name'],
            'requester_role': session['role'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'Pending'
        }
        blood_requests.append(new_request)
        print(f"New Blood Request: {new_request}") # Log to terminal
        flash('Blood request submitted successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('request_blood.html')

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Simple Access Control: Only Blood Bank or Hospital can edit, others view?
    # Prompt implies Blood Bank updates inventory.
    can_edit = session['role'] == 'blood_bank'

    if request.method == 'POST':
        if not can_edit:
            flash('Unauthorized action.', 'danger')
            return redirect(url_for('inventory'))
            
        blood_type = request.form.get('blood_type')
        quantity = int(request.form.get('quantity'))
        action = request.form.get('action') # add or remove

        # Find item
        item = next((i for i in blood_inventory if i['blood_type'] == blood_type), None)
        
        if action == 'add':
            if item:
                item['quantity'] += quantity
                item['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                blood_inventory.append({
                    'blood_type': blood_type,
                    'quantity': quantity,
                    'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            flash(f'Added {quantity} unit(s) of {blood_type}.', 'success')
            
        elif action == 'remove':
            if item and item['quantity'] >= quantity:
                item['quantity'] -= quantity
                item['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                flash(f'Removed {quantity} unit(s) of {blood_type}.', 'warning')
            else:
                flash('Insufficient stock!', 'danger')
        
        print(f"Inventory Updated: {blood_inventory}") # Log to terminal
        return redirect(url_for('inventory'))

    return render_template('inventory.html', inventory=blood_inventory, can_edit=can_edit)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
