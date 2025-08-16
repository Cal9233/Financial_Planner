# Personal Finance Management System - Setup & Run Instructions

## Prerequisites
- MySQL server installed and running
- Python 3.x installed
- Node.js and npm installed
- The Phase 1 database script executed in MySQL

## Quick Start

### Step 1: Start the Backend
```bash
cd Backend
python app.py
```
The backend will start on http://localhost:5000

### Step 2: Start the Frontend
Open a new terminal and run:
```bash
cd frontend
npm install  # Only needed first time
npm start
```
The frontend will start on http://localhost:3000

### Step 3: Connect and Use
1. Navigate to http://localhost:3000 in your browser
2. You'll be redirected to the database connection page
3. Enter your MySQL credentials:
   - Host: localhost (or your MySQL host)
   - Username: your_mysql_username
   - Password: your_mysql_password
   - Database: personal_finance_db
   - Port: 3306 (default)
4. Click "Test Connection" to verify
5. Click "Connect" to proceed
6. Register a new account or login

## Verification Tests

### Test Backend Health
```bash
curl http://localhost:5000/health
```

### Test Database Status
```bash
curl http://localhost:5000/api/database/status
```

### Test CORS Configuration
```bash
curl -I -X OPTIONS http://localhost:5000/api/database/status \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET"
```

## Connection Flow
1. **Frontend** → Makes API calls to Backend with credentials included
2. **Backend** → Verifies database connection stored in session
3. **Database** → Executes queries and returns data
4. **Backend** → Formats response and sends to Frontend
5. **Frontend** → Displays data with Material-UI components

## Troubleshooting

### Backend Issues
- Check if port 5000 is available
- Verify all Python dependencies are installed: `pip install -r requirements.txt`
- Check backend.log for errors

### Frontend Issues
- Check if port 3000 is available
- Clear browser cache and cookies
- Check browser console for errors

### Database Connection Issues
- Verify MySQL is running
- Check database credentials
- Ensure personal_finance_db exists
- Verify Phase 1 script was executed

## Features Available
- ✅ Database Connection Management
- ✅ User Registration/Login
- ✅ Dashboard with Charts
- ✅ Transaction Management
- 🔲 Account Management (scaffolded)
- 🔲 Budget Management (scaffolded)
- 🔲 Goal Tracking (scaffolded)
- 🔲 Reports & PDF Generation (scaffolded)

## Security Notes
- Database credentials are stored in server-side sessions
- JWT tokens expire after 24 hours
- All API endpoints require authentication (except database connection)
- CORS is configured for localhost:3000 only