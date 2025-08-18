# Personal Finance Management API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## Database Connection

### Connect to Database
- **POST** `/api/database/connect`
- Body: `{ host, user, password, database, port }`

### Check Connection Status
- **GET** `/api/database/status`

### Disconnect Database
- **POST** `/api/database/disconnect`

### Test Connection
- **POST** `/api/database/test`
- Body: `{ host, user, password, database, port }`

## Authentication

### Register
- **POST** `/api/auth/register`
- Body: `{ username, email, password, first_name, last_name }`

### Login
- **POST** `/api/auth/login`
- Body: `{ username, password }`

### Logout
- **POST** `/api/auth/logout`
- Requires: JWT

### Refresh Token
- **POST** `/api/auth/refresh`
- Header: `Authorization: Bearer <refresh_token>`

### Get Current User
- **GET** `/api/auth/me`
- **GET** `/api/users/profile`
- Requires: JWT

## Accounts

### List Accounts
- **GET** `/api/accounts`
- Requires: JWT

### Get Account
- **GET** `/api/accounts/{account_id}`
- Requires: JWT

### Create Account
- **POST** `/api/accounts`
- Body: `{ account_name, account_type, balance, institution, account_number }`
- Requires: JWT

### Update Account
- **PUT** `/api/accounts/{account_id}`
- Body: Any account fields to update
- Requires: JWT

### Delete Account
- **DELETE** `/api/accounts/{account_id}`
- Requires: JWT

## Transactions

### List Transactions
- **GET** `/api/transactions?page=1&per_page=10`
- Requires: JWT

### Get Transaction Summary
- **GET** `/api/transactions/summary?period=month`
- Requires: JWT

### Create Transaction
- **POST** `/api/transactions`
- Body: `{ account_id, category_id, transaction_date, amount, transaction_type, description }`
- Requires: JWT

### Update Transaction
- **PUT** `/api/transactions/{transaction_id}`
- Body: Any transaction fields to update
- Requires: JWT

### Delete Transaction
- **DELETE** `/api/transactions/{transaction_id}`
- Requires: JWT

## Categories

### List Categories
- **GET** `/api/categories?type=expense`
- Query params: `type` (income/expense/all)
- Requires: JWT

### Get Category
- **GET** `/api/categories/{category_id}`
- Requires: JWT

### Create Category
- **POST** `/api/categories`
- Body: `{ name, type, parent_id }`
- Requires: JWT

### Update Category
- **PUT** `/api/categories/{category_id}`
- Body: Any category fields to update
- Requires: JWT

### Delete Category
- **DELETE** `/api/categories/{category_id}`
- Requires: JWT

### Create Default Categories
- **POST** `/api/categories/batch`
- Requires: JWT

## Budgets

### List Budgets
- **GET** `/api/budgets`
- Requires: JWT

### Get Budget Performance
- **GET** `/api/budgets/performance`
- Requires: JWT

### Create Budget
- **POST** `/api/budgets`
- Body: `{ category_id, budget_amount, period_type, start_date }`
- Requires: JWT

### Update Budget
- **PUT** `/api/budgets/{budget_id}`
- Body: `{ budget_amount, period_type }`
- Requires: JWT

### Delete Budget
- **DELETE** `/api/budgets/{budget_id}`
- Requires: JWT

## Goals

### List Goals
- **GET** `/api/goals?include_completed=false`
- Requires: JWT

### Get Goal
- **GET** `/api/goals/{goal_id}`
- Requires: JWT

### Create Goal
- **POST** `/api/goals`
- Body: `{ goal_name, goal_type, target_amount, current_amount, target_date, description }`
- Requires: JWT

### Update Goal
- **PUT** `/api/goals/{goal_id}`
- Body: Any goal fields to update
- Requires: JWT

### Update Goal Progress
- **PUT** `/api/goals/{goal_id}/progress`
- Body: `{ current_amount }`
- Requires: JWT

### Delete Goal
- **DELETE** `/api/goals/{goal_id}`
- Requires: JWT

## Reports

### Monthly Report
- **GET** `/api/reports/monthly/{year}/{month}`
- Requires: JWT

### Yearly Report
- **GET** `/api/reports/yearly/{year}`
- Requires: JWT

### Expense Trends
- **GET** `/api/reports/expense-trends`
- Returns last 6 months of expense trends by category
- Requires: JWT

### Cashflow Report
- **GET** `/api/reports/cashflow?period=month`
- Query params: `period` (month/quarter/year)
- Requires: JWT

## Response Format

### Success Response
```json
{
  "data": { ... },
  "message": "Success message"
}
```

### Error Response
```json
{
  "error": "Error message"
}
```

### Pagination Response
```json
{
  "items": [ ... ],
  "total": 100,
  "page": 1,
  "per_page": 10
}
```