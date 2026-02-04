# BloodBridge: Optimizing Lifesaving Resources

**BloodBridge** is a comprehensive blood bank management system designed to seamlessly connect **Donors**, **Hospitals**, and **Blood Banks**. This project leverages modern web technologies to solve the critical issue of blood unavailability during emergencies.

---

## 📌 Project Overview
The primary goal of BloodBridge is to digitize and streamline the process of blood donation and inventory management. By providing a centralized platform, we ensure:
*   **Real-time Availability:** Hospitals can instantly check stock or broadcast needs.
*   **Rapid Response:** Donors receive notifications for urgent requests.
*   **Efficient Management:** Blood banks can maintain accurate digital inventories.

---

## 🌟 Key Features

### 1. User Roles & Access Control
*   **Donor:** 
    *   Register and Manage Profile.
    *   View "Active Blood Requests" from hospitals.
    *   Simple, one-click "Donate" action (Demostrative).
*   **Hospital:**
    *   Submit **Emergency Blood Requests** (Low, Medium, High, Critical).
    *   View available inventory across blood banks.
*   **Blood Bank Admin:**
    *   **Inventory Management:** Add, Remove, and Update blood stock.
    *   Monitor all requests and coordinate supply.

### 2. Core Functionalities
*   **Secure Authentication:** User Signup/Login with password hashing (SHA-256 via Werkzeug).
*   **Role-Based Dashboard:** Customized views for each user type.
*   **Flash Messages:** Instant feedback for user actions (Success/Error).
*   **Responsive UI:** Mobile-friendly design for access anywhere.

---

## 🧱 Tech Stack

### Frontend
*   **HTML5:** Semantic structure for accessibility.
*   **CSS3:** Custom styling with variables (`root`), Flexbox, and Grid for layouts.
*   **JavaScript:** Client-side validation using DOM manipulation.

### Backend
*   **Python Flask:** Lightweight WSGI web application framework.
*   **Jinja2:** Templating engine for dynamic HTML rendering.
*   **Werkzeug:** WSGI utility library for security (Password Hashing).

### AWS Cloud Integration (Deployment Phase)
*   **AWS EC2:** Virtual server for hosting the application.
*   **AWS DynamoDB:** NoSQL database for scalable data storage (Users, Requests, Inventory).
*   **AWS SNS:** Simple Notification Service for critical alerts via Email.

---

## 📁 Project Structure
```bash
BloodBridge/
│
├── app.py                  # LOCAL version (In-Memory Data)
├── aws_app.py              # AWS version (DynamoDB + SNS)
├── requirements.txt        # Python Dependencies
│
├── templates/              # HTML Templates
│   ├── layout.html         # Master Layout (Inheritance)
│   ├── index.html          # Landing Page
│   ├── dashboard.html      # Dynamic Dashboard
│   ├── inventory.html      # Inventory Management
│   ├── ...                 # (login, signup, request_blood, etc.)
│
├── static/
│   ├── css/style.css       # Global Stylesheet
│   └── js/script.js        # UI Interactions
│
└── README.md               # Project Documentation
```

---

## 🚀 Installation & Local Running Guide

### Prerequisites
*   Python 3.8+ installed.
*   pip (Python Package Manager).

### Step 1: Clone & Setup
```bash
# Navigate to project folder
cd BloodBridge/BloodBridge

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run Locally (In-Memory)
For local testing without AWS accounts, use `app.py`. Data resets when the server stops.
```bash
python app.py
```
*   **Access:** Open [http://localhost:5000](http://localhost:5000)

---

## ☁️ AWS Deployment Guide

To deploy the production-ready version with persistent storage and notifications:

### Step 1: AWS Configuration
1.  **Launch EC2 Instance:** Use Amazon Linux 2 or Ubuntu.
2.  **IAM Role:** Create a role with the following permissions and attach it to your EC2 instance:
    *   `AmazonDynamoDBFullAccess` (Read/Write to tables)
    *   `AmazonSNSFullAccess` (Send email alerts)

### Step 2: Database Setup (DynamoDB)
Create the following tables in `us-east-1` (or your configured region):
*   **BloodBridge_Users**: Partition Key: `email` (String)
*   **BloodBridge_Requests**: Partition Key: `request_id` (String)
*   **BloodBridge_Inventory**: Partition Key: `blood_type` (String)

### Step 3: Run on Server
Connect to your EC2 instance (via SSH or Connect) and run:
```bash
# 1. Update system & install python/git
sudo yum update -y
sudo yum install git python3 -y

# 2. Get the code (Replace with your repo)
git clone <YOUR_REPO_URL>
cd BloodBridge/BloodBridge

# 3. Install dependencies
pip3 install -r requirements.txt

# 4. Set Environment Variables (Optional, defaults exist)
export SNS_TOPIC_ARN="arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:YourTopic"

# 5. Run the AWS Application
python3 aws_app.py
```
*   **Access:** Open `http://<EC2-Public-IP>:5000` (Ensure Security Group allows port 5000).

---

## 🧪 Testing Scenarios

1.  **Registration Validation:**
    *   Try signing up with an existing email (Should fail).
    *   Sign up with mismatched passwords (Frontend validation).

2.  **Blood Request Flow:**
    *   Login as **Hospital**.
    *   Submit a **High Urgency** request.
    *   *Expected Result (AWS):* Data saved to DynamoDB `BloodBridge_Requests` and SNS Email sent.

3.  **Inventory Check:**
    *   Login as **Blood Bank**.
    *   Add 10 units of "O+".
    *   Login as **Hospital** and verify "O+" shows 10 units in the dashboard.

---

## 🔮 Future Roadmap
*   **Google Maps API:** Locate nearest blood bank visually.
*   **Chat System:** Direct Hospital-to-Donor communication.
*   **Mobile App:** React Native version for on-the-go access.
*   **Machine Learning:** Predict blood shortages based on historical data.

---

### 📞 Contact & Support
*   **Project Lead:** [Your Name]
*   **Email:** support@bloodbridge.com
*   **GitHub:** [Link to Repo]

*Developed for Cloud Computing Capstone Project.*
