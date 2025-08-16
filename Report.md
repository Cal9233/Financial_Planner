# Personal Finance Management System - Implementation Instructions

## Project Overview
Create a comprehensive Personal Finance Management System that allows users to track income, expenses, budgets, and financial goals. The system should provide analytics, PDF reporting, and a user-friendly interface.

## Phase 1: Database Implementation

### 1.1 Create Database Schema
Implement a MySQL database with the following 7 tables:

**Users Table:**
- Primary key: user_id (AUTO_INCREMENT)
- Fields: username, email, password_hash, created_at, is_active
- Include proper indexing on username and email

**Categories Table:**
- Primary key: category_id (AUTO_INCREMENT)
- Fields: user_id (FK), category_name, category_type (ENUM: 'income', 'expense'), is_active
- Foreign key relationship to Users table

**Accounts Table:**
- Primary key: account_id (AUTO_INCREMENT)
- Fields: user_id (FK), account_name, account_type (ENUM: 'checking', 'savings', 'credit', 'investment'), balance (DECIMAL 15,2), is_active
- Foreign key relationship to Users table

**Transactions Table (30+ rows required):**
- Primary key: transaction_id (AUTO_INCREMENT)
- Fields: user_id (FK), account_id (FK), category_id (FK), amount (DECIMAL 10,2), transaction_date, transaction_time, description, transaction_type (ENUM: 'income', 'expense')
- Multiple foreign key relationships

**Budgets Table:**
- Primary key: budget_id (AUTO_INCREMENT)
- Fields: user_id (FK), category_id (FK), budget_amount (DECIMAL 10,2), period_start (DATE), period_end (DATE), spent_amount (DECIMAL 10,2)
- Foreign key relationships to Users and Categories

**Financial_Goals Table:**
- Primary key: goal_id (AUTO_INCREMENT)
- Fields: user_id (FK), goal_name, target_amount (DECIMAL 15,2), current_amount (DECIMAL 15,2), target_date, goal_type (ENUM), priority_level (ENUM), is_completed (BOOLEAN)

**Transaction_Splits Table:**
- Composite primary key: (transaction_id, split_number)
- Fields: transaction_id (FK), split_number, category_id (FK), amount (DECIMAL 10,2)
- Foreign key relationship to Transactions and Categories

### 1.2 Create Database Views
Implement two aggregating views:

**Monthly_Expense_Summary View:**
```sql
-- Aggregate monthly expenses/income by category
-- Use COUNT, SUM, AVG, MIN, MAX functions
-- Group by user, year, month, category
-- Order by total amount
```

**Budget_Performance_Analysis View:**
```sql
-- Compare actual spending against budgets
-- Calculate remaining budget, utilization percentages
-- Include status indicators (Over Budget, Near Limit, Within Budget)
-- Show days remaining in budget period
```

### 1.3 Create Functions and Stored Procedures

**Lookup Functions (return -1 if not found):**
1. `GetUserIdByUsername(username VARCHAR(50))`
2. `GetCategoryIdByName(user_id INT, category_name VARCHAR(100))`
3. `GetAccountIdByName(user_id INT, account_name VARCHAR(100))`
4. `GetBudgetIdByUserCategory(user_id INT, category_id INT, period_date DATE)`
5. `GetGoalIdByName(user_id INT, goal_name VARCHAR(100))`

**Data Retrieval Procedures:**
1. `GetUsers(show_inactive BOOLEAN)`
2. `GetCategoriesByUser(user_id INT)`
3. `GetAccountsByUser(user_id INT)`
4. `GetTransactions(user_id INT, limit_count INT, offset_count INT)`
5. `GetBudgetsByUser(user_id INT)`
6. `GetGoalsByUser(user_id INT)`

**Data Modification Procedures:**
1. `UpdateBudget(budget_id INT, new_amount DECIMAL(10,2))` - with cascading recalculations
2. `DeleteTransaction(transaction_id INT)` - with cascading deletions and balance updates

### 1.4 Load Sample Data
- Create at least 3 test users
- Add 10+ categories per user (mix of income/expense)
- Create 3+ accounts per user with realistic balances
- Insert 30+ transactions across multiple users and time periods
- Add budget data for various categories
- Include 5+ financial goals with different completion statuses

## Phase 2: Backend Development (Flask)

### 2.1 Set Up Flask Application
Create a Flask application with the following structure:
- Flask 2.3 with Flask-SQLAlchemy
- JWT authentication system
- Flask-CORS for frontend integration
- Error handling and logging

### 2.2 Create API Endpoints
Implement RESTful API endpoints for:

**Authentication:**
- POST /api/auth/login
- POST /api/auth/register
- POST /api/auth/logout

**Users:**
- GET /api/users/profile
- PUT /api/users/profile

**Categories:**
- GET /api/categories
- POST /api/categories
- PUT /api/categories/{id}
- DELETE /api/categories/{id}

**Accounts:**
- GET /api/accounts
- POST /api/accounts
- PUT /api/accounts/{id}
- DELETE /api/accounts/{id}

**Transactions:**
- GET /api/transactions (with pagination)
- POST /api/transactions
- PUT /api/transactions/{id}
- DELETE /api/transactions/{id}
- GET /api/transactions/summary

**Budgets:**
- GET /api/budgets
- POST /api/budgets
- PUT /api/budgets/{id}
- DELETE /api/budgets/{id}
- GET /api/budgets/performance

**Goals:**
- GET /api/goals
- POST /api/goals
- PUT /api/goals/{id}
- DELETE /api/goals/{id}

**Reports:**
- GET /api/reports/monthly/{year}/{month}
- GET /api/reports/pdf/{year}/{month}

### 2.3 Implement PDF Report Generation
Using ReportLab, create comprehensive monthly financial reports including:
- Spending summaries by category with charts
- Budget performance analysis
- Goal progress tracking
- Account balance trends
- Transaction history

## Phase 3: Frontend Development (React)

### 3.1 Set Up React Application
- React.js 18 with Material-UI components
- React Router for navigation
- State management (Context API or Redux)
- Chart.js integration for data visualization

### 3.2 Create React Components

**Authentication Components:**
- Login form
- Registration form
- Protected route wrapper

**Dashboard Components:**
- Overview dashboard with key metrics
- Spending summary charts
- Recent transactions list
- Quick action buttons

**Transaction Management:**
- Transaction list with filtering/sorting
- Add/edit transaction forms
- Transaction categorization
- Split transaction handling

**Budget Management:**
- Budget overview with progress bars
- Budget creation/editing forms
- Budget vs actual spending charts
- Alert system for budget limits

**Goal Management:**
- Goals dashboard with progress indicators
- Goal creation/editing forms
- Goal tracking visualizations

**Account Management:**
- Account balance overview
- Account transaction history
- Account management forms

**Reports:**
- Monthly report viewer
- PDF download functionality
- Interactive charts and graphs
- Export capabilities

### 3.3 Implement Data Visualization
Using Chart.js, create:
- Pie charts for expense categorization
- Line charts for spending trends
- Bar charts for budget comparisons
- Progress indicators for goals

## Phase 4: Testing Implementation

### 4.1 Unit Testing
- Test all stored procedures with diverse sample data
- Test API endpoints with various input scenarios
- Test frontend components with mock data
- Use pytest for backend testing, Jest for frontend

### 4.2 Integration Testing
- Test database-backend integration
- Test backend-frontend API communication
- Verify view calculations and aggregations
- Test cascading operations (updates/deletes)

### 4.3 User Acceptance Testing
- Create test scenarios for typical user workflows
- Test UI/UX intuition and error handling
- Verify PDF report generation quality
- Test responsive design across devices

### 4.4 Performance Testing
- Test with large datasets (100+ transactions)
- Verify query performance with indexes
- Test concurrent user scenarios
- Monitor memory usage and response times

## Phase 5: Security and Deployment

### 5.1 Security Implementation
- JWT token management
- Password hashing and validation
- SQL injection prevention
- XSS protection
- HTTPS enforcement
- Input validation and sanitization

### 5.2 Deployment Preparation
- Environment configuration management
- Database backup and recovery procedures
- Error logging and monitoring
- Performance monitoring setup

## Deliverables

1. Complete database schema with sample data
2. Fully functional Flask backend API
3. React frontend application
4. PDF report generation system
5. Comprehensive test suite
6. Documentation and user guide
7. Deployment scripts and configuration

## Success Criteria

- All database requirements met (7 tables, composite keys, foreign keys, views, procedures)
- 30+ transactions in sample data
- Two functional aggregate views
- Complete API coverage for all operations
- Responsive frontend with data visualization
- PDF report generation working
- All tests passing
- Clean, maintainable code structure

## Timeline
- Database Implementation: 2 weeks
- Backend Development: 1 week
- Frontend Development: 1 week
- PDF Feature Integration: 1 week
- Testing and Debugging: 1 week
- Final Adjustments: 1 week
