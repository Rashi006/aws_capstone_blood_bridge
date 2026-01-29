# BloodBridge: Optimizing Lifesaving Resources

**BloodBridge** is a web-based blood bank management system designed to connect donors, hospitals, and blood banks efficiently. This academic mini-project demonstrates a full-stack web application using Flask, HTML, CSS, and JavaScript.

## 📌 Project Overview
BloodBridge aims to solve the problem of blood unavailability during emergencies by providing a centralized platform where:
- **Donors** can view urgent requests and register to donate.
- **Hospitals** can broadcast emergency blood requirements.
- **Blood Banks** can manage their inventory and coordinate with hospitals.

## 🧱 Tech Stack
- **Frontend:**
  - HTML5 (Structure)
  - CSS3 (Styling & Responsive Design)
  - JavaScript (Client-side Logic)
- **Backend:**
  - Python Flask (Web Framework)
  - Werkzeug Security (Password Hashing)
  - Flask Session (Authentication)
- **Data Storage:**
  - In-Memory Python Lists & Dictionaries (Phase 1)

## 📁 Project Structure
```
BloodBridge/
│
├── app.py                  # Main Flask Application
│
├── templates/              # HTML Templates
│   ├── layout.html         # Base template
│   ├── index.html          # Home
│   ├── login.html          # Authentication
│   ├── signup.html         # Registration
│   ├── dashboard.html      # Role-based Dashboard
│   ├── request_blood.html  # Request Form
│   ├── inventory.html      # Inventory Management
│   ├── about.html          # About Page
│   ├── contact.html        # Contact Page
│
├── static/
│   ├── css/style.css       # Stylesheets
│   └── js/script.js        # JavaScript
│
└── README.md               # Documentation
```

## 🚀 How to Run the Project (Locally)
1.  **Prerequisites:**
    - Python 3.x installed.
    - Flask installed (`pip install flask`).

2.  **Setup:**
    Navigate to the project directory:
    ```bash
    cd BloodBridge
    ```

3.  **Run the Application:**
    Execute the following command in your terminal:
    ```bash
    python app.py
    ```

4.  **Access Web App:**
    Open your browser and visit: `http://localhost:5000`

## 🧪 Testing Steps
1.  **Register:** Go to `/signup` and create accounts for different roles (Donor, Hospital, Blood Bank).
2.  **Login:** Use credentials to log in.
3.  **Dashboard:** Check the customized dashboard for each role.
4.  **Action:**
    - As **Hospital**: Submit a blood request.
    - As **Blood Bank**: Add items to inventory via `/inventory`.
    - As **Donor**: View the dashboard to see active requests.
5.  **Verify:** Check the terminal output to see logged data (users, requests, inventory).

## 🔮 Future Scope
- **Database Integration:** Migrate from in-memory lists to **AWS DynamoDB** or **PostgreSQL** for persistent storage.
- **Cloud Deployment:** Host the application on **AWS EC2** for global access.
- **Real-time Notifications:** Implement SMS/Email alerts using **AWS SNS**.
- **Advanced Analytics:** Data visualization for blood demand and supply trends.

---
*Created for Academic Mini-Project Submission.*
