# Personal Finance Management System

A comprehensive web-based personal finance management application built with React, Flask, and MySQL. This system allows users to track income, expenses, budgets, and financial goals with data visualization and PDF reporting capabilities.

## 🚀 Quick Start Guide

### Prerequisites
- **MySQL** 5.7+ installed and running
- **Python** 3.8+ installed
- **Node.js** 14+ and npm installed
- **Git** (for cloning the repository)

### Installation & Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/Cal9233/Financial_Planner.git
cd CSC6302_Final
```

#### 2. Set Up the Database (Phase 1)
```bash
# Log into MySQL
mysql -u root -p

# Run the database script
mysql> source Database/DatabaseScript.sql
```
This creates the `personal_finance_db` database with all required tables, views, and procedures.

#### 3. Set Up the Backend (Phase 2)
```bash
# Navigate to backend directory
cd Backend

# Install Python dependencies
pip install -r requirements.txt

# Create a .env file (optional)
cp .env.example .env
# Edit .env with your preferences (optional)
```

#### 4. Set Up the Frontend (Phase 3)
```bash
# Navigate to Frontend directory
cd ../Frontend

# Install Node dependencies
npm install
```

## 🏃‍♂️ Running the Application

### Step 1: Start the Backend Server
```bash
# From the Backend directory
cd Backend
python app.py
```
The backend will start at `http://localhost:5000`

### Step 2: Start the Frontend Server
Open a new terminal window:
```bash
# From the frontend directory
cd frontend
npm start
```
The frontend will start at `http://localhost:3000` and automatically open in your browser.

### Step 3: Connect to Your Database
1. Navigate to `http://localhost:3000` in your browser
2. You'll see the database connection screen
3. Enter your MySQL credentials:
   - **Host**: localhost
   - **Username**: your_mysql_username
   - **Password**: your_mysql_password
   - **Database**: personal_finance_db
   - **Port**: 3306 (default)
4. Click "Test Connection" to verify
5. Click "Connect" to proceed

### Step 4: Create an Account
1. Click "Register here" on the login page
2. Fill in your information
3. Start managing your finances!

## 📊 Features

### ✅ Implemented
- **Database Connection Management** - Dynamic MySQL connection with secure cookie-based session storage
- **User Authentication** - Secure registration/login with JWT tokens
- **Dashboard** - Financial overview with charts and summaries
- **Transaction Management** - Add, edit, delete, and filter transactions
- **Data Visualization** - Pie charts for expense categories using Chart.js
- **Responsive Design** - Works on desktop and mobile devices

### 🔲 Ready for Enhancement
- Account Management
- Budget Creation & Tracking
- Financial Goal Management
- PDF Report Generation

## 🏗️ Project Structure
```
CSC6302_Final/
├── Database/               # Phase 1: MySQL database scripts
│   └── DatabaseScript.sql  # Complete database schema
├── Backend/                # Phase 2: Flask API
│   ├── app.py             # Main application file
│   ├── models/            # Database models
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   └── requirements.txt   # Python dependencies
└── frontend/              # Phase 3: React application
    ├── src/
    │   ├── components/    # React components
    │   ├── contexts/      # React contexts
    │   ├── services/      # API services
    │   └── types/         # TypeScript types
    └── package.json       # Node dependencies
```

## 🧪 Testing the Connection

### Verify Backend Health
```bash
curl http://localhost:5000/health
```

### Check Database Connection Status
```bash
curl http://localhost:5000/api/database/status
```

### Test CORS Configuration
```bash
curl -I -X OPTIONS http://localhost:5000/api/database/status \
  -H "Origin: http://localhost:3000"
```

## 🐛 Troubleshooting

### Backend Won't Start
- Ensure port 5000 is not in use: `lsof -i :5000`
- Check Python version: `python --version` (needs 3.8+)
- Verify all dependencies: `pip install -r requirements.txt`

### Frontend Won't Start
- Ensure port 3000 is not in use: `lsof -i :3000`
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### Database Connection Failed
- Verify MySQL is running: `sudo service mysql status`
- Check credentials are correct
- Ensure database exists: `mysql -u root -p -e "SHOW DATABASES;"`
- Verify firewall allows MySQL connections

### CORS Errors
- Ensure backend is running before frontend
- Check browser console for specific error messages
- Verify frontend URL in backend CORS configuration

## 🔒 Security Notes
- Database credentials are stored in encrypted cookie-based sessions
- Passwords are hashed using Werkzeug security
- JWT tokens expire after 24 hours
- All API endpoints require authentication (except database connection)
- CORS is restricted to specific origins
- Session cookies are HttpOnly and use SameSite protection

## 📚 API Documentation

### Database Endpoints
- `POST /api/database/connect` - Connect to MySQL database
- `GET /api/database/status` - Check connection status

### Authentication Endpoints
- `POST /api/auth/register` - Create new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Protected Endpoints (require authentication)
- `GET /api/transactions` - List transactions
- `POST /api/transactions` - Create transaction
- `GET /api/accounts` - List accounts
- `GET /api/categories` - List categories
- `GET /api/budgets` - List budgets
- `GET /api/goals` - List financial goals

## 👥 Contributors
- Calvin Malagon - [GitHub](https://github.com/Cal9233)

## 📝 License
This project is part of academic coursework for CSC6302.