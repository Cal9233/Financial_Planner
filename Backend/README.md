# Personal Finance Management System - Backend

## Phase 2: Flask Backend Implementation

This is the Flask backend API for the Personal Finance Management System. It provides RESTful endpoints for managing users, accounts, transactions, budgets, and financial goals.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Update the database credentials and secret keys in `.env`

3. **Database Setup**
   - Ensure MySQL is running
   - The database should already be created from Phase 1
   - Tables will be verified/created when the app starts

4. **Run the Application**
   ```bash
   python app.py
   ```

## API Endpoints

### Database Connection
- `POST /api/database/connect` - Connect to MySQL database
- `POST /api/database/disconnect` - Disconnect from database
- `GET /api/database/status` - Check connection status
- `POST /api/database/test` - Test connection without saving

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh access token

### Users
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create new category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

### Accounts
- `GET /api/accounts` - Get all accounts
- `POST /api/accounts` - Create new account
- `PUT /api/accounts/{id}` - Update account
- `DELETE /api/accounts/{id}` - Delete account

### Transactions
- `GET /api/transactions` - Get transactions (paginated)
- `POST /api/transactions` - Create new transaction
- `PUT /api/transactions/{id}` - Update transaction
- `DELETE /api/transactions/{id}` - Delete transaction
- `GET /api/transactions/summary` - Get transaction summary

### Budgets
- `GET /api/budgets` - Get all budgets
- `POST /api/budgets` - Create new budget
- `PUT /api/budgets/{id}` - Update budget
- `DELETE /api/budgets/{id}` - Delete budget
- `GET /api/budgets/performance` - Get budget performance

### Goals
- `GET /api/goals` - Get all goals
- `POST /api/goals` - Create new goal
- `PUT /api/goals/{id}` - Update goal
- `DELETE /api/goals/{id}` - Delete goal
- `POST /api/goals/{id}/contribute` - Add contribution to goal

### Reports
- `GET /api/reports/monthly/{year}/{month}` - Get monthly report data
- `GET /api/reports/pdf/{year}/{month}` - Download monthly PDF report

## Features Implemented

1. **JWT Authentication** - Secure token-based authentication
2. **RESTful API** - Clean and consistent API design
3. **Data Validation** - Input validation on all endpoints
4. **Error Handling** - Comprehensive error handling
5. **PDF Generation** - Monthly financial reports in PDF format
6. **Database Integration** - Full integration with MySQL database from Phase 1
7. **CORS Support** - Cross-origin resource sharing for frontend integration

## Testing

Use tools like Postman or curl to test the endpoints:

```bash
# First, connect to the database
curl -X POST http://localhost:5000/api/database/connect \
  -H "Content-Type: application/json" \
  -d '{"host":"localhost","user":"root","password":"your_password","database":"personal_finance_db"}'

# Then register a new user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123","first_name":"Test","last_name":"User"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

## Dynamic Database Connection

The backend now supports dynamic database connections. Users must provide their MySQL credentials through the frontend, which will be stored securely in the session. The workflow is:

1. User provides database credentials via frontend
2. Backend tests the connection
3. If successful, credentials are stored in session
4. All subsequent API calls use the stored connection
5. Connection persists for 7 days or until logout

## Security Notes

- All passwords are hashed using Werkzeug's security functions
- JWT tokens expire after 24 hours
- Sensitive endpoints require authentication
- Input validation prevents SQL injection
- CORS is configured for specific origins only