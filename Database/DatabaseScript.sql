-- Personal Finance Management System Database - Complete Implementation
-- Updated to meet all requirements

DROP DATABASE IF EXISTS personal_finance_db;
CREATE DATABASE personal_finance_db;
USE personal_finance_db;

-- Create Users table
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active TINYINT(1) DEFAULT 1,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_active_users (is_active)
);

-- Create Categories table
CREATE TABLE Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_name VARCHAR(50) NOT NULL,
    category_type ENUM('income', 'expense') NOT NULL,
    description TEXT,
    color_code VARCHAR(7),
    is_active TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    INDEX idx_user_categories (user_id),
    INDEX idx_category_type (category_type),
    UNIQUE KEY unique_user_category (user_id, category_name)
);

-- Create Accounts table
CREATE TABLE Accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type ENUM('checking', 'savings', 'credit', 'investment') NOT NULL,
    balance DECIMAL(15,2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'USD',
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active TINYINT(1) DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    INDEX idx_user_accounts (user_id),
    INDEX idx_account_type (account_type),
    INDEX idx_active_accounts (is_active)
);

-- Create Transactions table (largest table - will have 30+ rows)
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255),
    transaction_date DATE NOT NULL,
    transaction_time TIME DEFAULT '12:00:00',
    transaction_type ENUM('income', 'expense', 'transfer') NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'completed',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE RESTRICT,
    INDEX idx_account_transactions (account_id),
    INDEX idx_category_transactions (category_id),
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_transaction_type (transaction_type),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Create Budgets table
CREATE TABLE Budgets (
    budget_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    budget_amount DECIMAL(10,2) NOT NULL,
    spent_amount DECIMAL(10,2) DEFAULT 0.00,
    period_type ENUM('weekly', 'monthly', 'yearly') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE,
    INDEX idx_user_budgets (user_id),
    INDEX idx_category_budgets (category_id),
    INDEX idx_budget_period (start_date, end_date),
    INDEX idx_active_budgets (is_active),
    UNIQUE KEY unique_user_category_period (user_id, category_id, start_date, end_date)
);

-- Create Financial_Goals table
CREATE TABLE Financial_Goals (
    goal_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    goal_name VARCHAR(100) NOT NULL,
    target_amount DECIMAL(15,2) NOT NULL,
    current_amount DECIMAL(15,2) DEFAULT 0.00,
    target_date DATE,
    goal_type ENUM('savings', 'debt_payoff', 'investment') NOT NULL,
    priority_level ENUM('low', 'medium', 'high') DEFAULT 'medium',
    description TEXT,
    is_completed TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    INDEX idx_user_goals (user_id),
    INDEX idx_goal_type (goal_type),
    INDEX idx_target_date (target_date),
    INDEX idx_priority (priority_level),
    INDEX idx_created_at (created_at)
);

-- Create Transaction_Splits table (composite primary key)
CREATE TABLE Transaction_Splits (
    transaction_id INT NOT NULL,
    split_number INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255),
    PRIMARY KEY (transaction_id, split_number),
    FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE RESTRICT,
    INDEX idx_category_splits (category_id)
);

-- Insert Users
INSERT INTO Users (username, email, password_hash, first_name, last_name, last_login) VALUES 
('john_doe', 'john@example.com', 'hashed_password_123', 'John', 'Doe', '2024-01-15 08:30:00'),
('jane_smith', 'jane@example.com', 'hashed_password_456', 'Jane', 'Smith', '2024-01-14 19:45:00'),
('mike_wilson', 'mike@example.com', 'hashed_password_789', 'Mike', 'Wilson', '2024-01-13 14:20:00'),
('sarah_johnson', 'sarah@example.com', 'hashed_password_101', 'Sarah', 'Johnson', '2024-01-16 11:15:00');

-- Insert Categories
INSERT INTO Categories (user_id, category_name, category_type, description, color_code) VALUES 
-- User 1 categories
(1, 'Salary', 'income', 'Monthly salary income', '#4CAF50'),
(1, 'Bonus', 'income', 'Performance bonuses', '#8BC34A'),
(1, 'Groceries', 'expense', 'Food and grocery expenses', '#FF5722'),
(1, 'Transportation', 'expense', 'Gas, public transport, car maintenance', '#2196F3'),
(1, 'Entertainment', 'expense', 'Movies, dining out, hobbies', '#FF9800'),
(1, 'Utilities', 'expense', 'Electricity, water, internet, phone', '#607D8B'),
(1, 'Healthcare', 'expense', 'Medical expenses and insurance', '#9C27B0'),
-- User 2 categories
(2, 'Freelance', 'income', 'Freelance project income', '#4CAF50'),
(2, 'Investment', 'income', 'Dividend and investment returns', '#00BCD4'),
(2, 'Rent', 'expense', 'Monthly rent payment', '#F44336'),
(2, 'Food', 'expense', 'Dining and groceries', '#FF5722'),
(2, 'Shopping', 'expense', 'Clothing and misc purchases', '#E91E63'),
-- User 3 categories
(3, 'Part-time Job', 'income', 'Part-time work income', '#4CAF50'),
(3, 'Housing', 'expense', 'Rent and utilities', '#795548'),
(3, 'Education', 'expense', 'Books and school supplies', '#3F51B5'),
-- User 4 categories
(4, 'Consulting', 'income', 'Consulting fees', '#4CAF50'),
(4, 'Travel', 'expense', 'Business and personal travel', '#FF9800');

-- Insert Accounts
INSERT INTO Accounts (user_id, account_name, account_type, balance) VALUES 
(1, 'Main Checking', 'checking', 5000.00),
(1, 'Emergency Savings', 'savings', 10000.00),
(1, 'Credit Card', 'credit', -2500.00),
(1, 'Investment Portfolio', 'investment', 25000.00),
(2, 'Business Checking', 'checking', 3500.00),
(2, 'High Yield Savings', 'savings', 8000.00),
(2, 'Investment Account', 'investment', 15000.00),
(3, 'Student Checking', 'checking', 1200.00),
(3, 'Savings', 'savings', 2500.00),
(4, 'Consulting Account', 'checking', 7500.00);

-- Insert extensive Transactions data (30+ rows)
INSERT INTO Transactions (account_id, category_id, amount, description, transaction_date, transaction_time, transaction_type, status) VALUES 
-- January 2024 transactions
(1, 1, 4000.00, 'Monthly salary deposit', '2024-01-01', '09:00:00', 'income', 'completed'),
(1, 3, -150.00, 'Weekly groceries at Walmart', '2024-01-02', '14:30:00', 'expense', 'completed'),
(1, 4, -45.00, 'Gas station fill-up', '2024-01-03', '08:15:00', 'expense', 'completed'),
(1, 5, -80.00, 'Movie theater and dinner', '2024-01-05', '19:30:00', 'expense', 'completed'),
(1, 6, -120.00, 'Electric bill payment', '2024-01-06', '10:00:00', 'expense', 'completed'),
(1, 3, -95.00, 'Grocery store trip', '2024-01-08', '16:45:00', 'expense', 'completed'),
(1, 4, -40.00, 'Public transport monthly pass', '2024-01-10', '07:30:00', 'expense', 'completed'),
(1, 7, -200.00, 'Doctor visit copay', '2024-01-12', '11:20:00', 'expense', 'completed'),
(1, 5, -60.00, 'Concert tickets', '2024-01-15', '20:00:00', 'expense', 'completed'),
(1, 6, -85.00, 'Internet bill', '2024-01-16', '09:45:00', 'expense', 'completed'),

-- User 2 transactions
(5, 8, 800.00, 'Web development project', '2024-01-04', '16:00:00', 'income', 'completed'),
(5, 10, -1200.00, 'January rent payment', '2024-01-05', '08:00:00', 'expense', 'completed'),
(5, 11, -200.00, 'Grocery shopping', '2024-01-06', '15:20:00', 'expense', 'completed'),
(5, 8, 1200.00, 'Mobile app project', '2024-01-10', '17:30:00', 'income', 'completed'),
(5, 12, -150.00, 'New winter jacket', '2024-01-12', '13:45:00', 'expense', 'completed'),
(5, 11, -180.00, 'Restaurant and groceries', '2024-01-14', '18:00:00', 'expense', 'completed'),
(6, 9, 150.00, 'Dividend payment', '2024-01-15', '10:00:00', 'income', 'completed'),

-- User 3 transactions
(8, 13, 600.00, 'Part-time work pay', '2024-01-07', '14:00:00', 'income', 'completed'),
(8, 14, -450.00, 'Monthly rent portion', '2024-01-08', '09:00:00', 'expense', 'completed'),
(8, 15, -80.00, 'Textbooks purchase', '2024-01-10', '12:30:00', 'expense', 'completed'),
(8, 14, -60.00, 'Utilities share', '2024-01-12', '16:00:00', 'expense', 'completed'),

-- User 4 transactions
(10, 16, 2500.00, 'Marketing consulting fee', '2024-01-09', '11:00:00', 'income', 'completed'),
(10, 17, -800.00, 'Business trip to Chicago', '2024-01-11', '06:30:00', 'expense', 'completed'),
(10, 17, -300.00, 'Client dinner expense', '2024-01-13', '19:45:00', 'expense', 'completed'),

-- More transactions for February
(1, 1, 4000.00, 'February salary', '2024-02-01', '09:00:00', 'income', 'completed'),
(1, 2, 500.00, 'Performance bonus', '2024-02-05', '09:00:00', 'income', 'completed'),
(1, 3, -160.00, 'Weekly groceries', '2024-02-02', '15:00:00', 'expense', 'completed'),
(1, 4, -55.00, 'Gas and car wash', '2024-02-03', '10:30:00', 'expense', 'completed'),
(1, 5, -120.00, 'Weekend entertainment', '2024-02-04', '20:15:00', 'expense', 'completed'),
(2, 1, 1000.00, 'Savings transfer', '2024-02-06', '14:00:00', 'transfer', 'completed'),
(5, 8, 900.00, 'February freelance work', '2024-02-07', '15:30:00', 'income', 'completed'),
(8, 13, 650.00, 'February part-time pay', '2024-02-08', '13:45:00', 'income', 'completed'),
(10, 16, 3000.00, 'Large consulting project', '2024-02-09', '16:20:00', 'income', 'completed'),

-- Additional transactions to reach 30+
(1, 3, -85.00, 'Mid-week grocery run', '2024-02-10', '17:30:00', 'expense', 'completed'),
(1, 6, -95.00, 'Phone bill', '2024-02-11', '11:15:00', 'expense', 'completed'),
(5, 11, -220.00, 'Weekly food expenses', '2024-02-12', '19:00:00', 'expense', 'completed'),
(8, 15, -120.00, 'School supplies and lab fee', '2024-02-13', '14:30:00', 'expense', 'completed');

-- Insert Budget data
INSERT INTO Budgets (user_id, category_id, budget_amount, spent_amount, period_type, start_date, end_date) VALUES 
(1, 3, 600.00, 490.00, 'monthly', '2024-01-01', '2024-01-31'),
(1, 4, 200.00, 140.00, 'monthly', '2024-01-01', '2024-01-31'),
(1, 5, 300.00, 260.00, 'monthly', '2024-01-01', '2024-01-31'),
(1, 6, 300.00, 300.00, 'monthly', '2024-01-01', '2024-01-31'),
(2, 10, 1200.00, 1200.00, 'monthly', '2024-01-01', '2024-01-31'),
(2, 11, 500.00, 600.00, 'monthly', '2024-01-01', '2024-01-31'),
(3, 14, 600.00, 510.00, 'monthly', '2024-01-01', '2024-01-31'),
(4, 17, 1000.00, 1100.00, 'monthly', '2024-01-01', '2024-01-31');

-- Insert Financial Goals
INSERT INTO Financial_Goals (user_id, goal_name, target_amount, current_amount, target_date, goal_type, priority_level, description) VALUES 
(1, 'Emergency Fund', 20000.00, 10000.00, '2024-12-31', 'savings', 'high', 'Build 6-month emergency fund'),
(1, 'Vacation Fund', 5000.00, 1200.00, '2024-07-01', 'savings', 'medium', 'Summer vacation to Europe'),
(1, 'Car Down Payment', 8000.00, 2500.00, '2024-09-30', 'savings', 'medium', 'Down payment for new car'),
(2, 'Investment Portfolio', 50000.00, 15000.00, '2025-12-31', 'investment', 'high', 'Build diversified investment portfolio'),
(2, 'Home Down Payment', 40000.00, 8000.00, '2025-06-30', 'savings', 'high', '20% down payment for house'),
(3, 'Student Loan Payoff', 15000.00, 3000.00, '2026-05-31', 'debt_payoff', 'high', 'Pay off remaining student loans'),
(4, 'Business Expansion', 25000.00, 7500.00, '2024-08-31', 'investment', 'high', 'Fund for expanding consulting business');

-- Insert Transaction Splits data (demonstrating composite primary key)
INSERT INTO Transaction_Splits (transaction_id, split_number, category_id, amount, description) VALUES 
(3, 1, 4, -30.00, 'Gas portion'),
(3, 2, 7, -15.00, 'Car wash portion'),
(9, 1, 5, -40.00, 'Concert ticket'),
(9, 2, 11, -20.00, 'Parking fee'),
(23, 1, 17, -600.00, 'Flight tickets'),
(23, 2, 17, -200.00, 'Hotel accommodation'),
(30, 1, 11, -180.00, 'Restaurant meal'),
(30, 2, 5, -40.00, 'Entertainment/tips');

-- ========================================
-- VIEWS (At least two views with aggregates)
-- ========================================

-- View 1: Monthly Expense Summary by Category
CREATE VIEW Monthly_Expense_Summary AS
SELECT 
    u.user_id,
    u.username,
    YEAR(t.transaction_date) as year,
    MONTH(t.transaction_date) as month,
    c.category_name,
    c.category_type,
    COUNT(t.transaction_id) as transaction_count,
    SUM(ABS(t.amount)) as total_amount,
    AVG(ABS(t.amount)) as average_amount,
    MIN(ABS(t.amount)) as min_amount,
    MAX(ABS(t.amount)) as max_amount
FROM Users u
JOIN Accounts a ON u.user_id = a.user_id
JOIN Transactions t ON a.account_id = t.account_id
JOIN Categories c ON t.category_id = c.category_id
WHERE t.transaction_type IN ('expense', 'income')
    AND t.status = 'completed'
GROUP BY u.user_id, u.username, YEAR(t.transaction_date), MONTH(t.transaction_date), c.category_id, c.category_name, c.category_type
ORDER BY u.username, year DESC, month DESC, total_amount DESC;

-- View 2: Budget Performance Analysis
CREATE VIEW Budget_Performance_Analysis AS
SELECT 
    u.user_id,
    u.username,
    b.budget_id,
    c.category_name,
    b.budget_amount,
    b.spent_amount,
    b.period_type,
    b.start_date,
    b.end_date,
    ROUND((b.spent_amount / b.budget_amount) * 100, 2) as utilization_percentage,
    (b.budget_amount - b.spent_amount) as remaining_budget,
    CASE 
        WHEN b.spent_amount > b.budget_amount THEN 'Over Budget'
        WHEN b.spent_amount >= (b.budget_amount * 0.8) THEN 'Near Limit'
        ELSE 'Within Budget'
    END as budget_status,
    DATEDIFF(b.end_date, CURDATE()) as days_remaining
FROM Users u
JOIN Budgets b ON u.user_id = b.user_id
JOIN Categories c ON b.category_id = c.category_id
WHERE b.is_active = 1
ORDER BY u.username, utilization_percentage DESC;

-- ========================================
-- FUNCTIONS (Return key or -1 if not found)
-- ========================================

DELIMITER //

-- Function to get User ID by username
CREATE FUNCTION GetUserIdByUsername(p_username VARCHAR(50))
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE user_id_result INT DEFAULT -1;
    
    SELECT user_id INTO user_id_result
    FROM Users
    WHERE username = p_username
    LIMIT 1;
    
    RETURN IFNULL(user_id_result, -1);
END//

-- Function to get Category ID by name and user
CREATE FUNCTION GetCategoryIdByName(p_user_id INT, p_category_name VARCHAR(50))
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE category_id_result INT DEFAULT -1;
    
    SELECT category_id INTO category_id_result
    FROM Categories
    WHERE user_id = p_user_id AND category_name = p_category_name
    LIMIT 1;
    
    RETURN IFNULL(category_id_result, -1);
END//

-- Function to get Account ID by name and user
CREATE FUNCTION GetAccountIdByName(p_user_id INT, p_account_name VARCHAR(100))
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE account_id_result INT DEFAULT -1;
    
    SELECT account_id INTO account_id_result
    FROM Accounts
    WHERE user_id = p_user_id AND account_name = p_account_name
    LIMIT 1;
    
    RETURN IFNULL(account_id_result, -1);
END//

-- Function to get Budget ID by user and category
CREATE FUNCTION GetBudgetIdByUserCategory(p_user_id INT, p_category_id INT, p_start_date DATE)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE budget_id_result INT DEFAULT -1;
    
    SELECT budget_id INTO budget_id_result
    FROM Budgets
    WHERE user_id = p_user_id AND category_id = p_category_id AND start_date = p_start_date
    LIMIT 1;
    
    RETURN IFNULL(budget_id_result, -1);
END//

-- Function to get Goal ID by user and goal name
CREATE FUNCTION GetGoalIdByName(p_user_id INT, p_goal_name VARCHAR(100))
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE goal_id_result INT DEFAULT -1;
    
    SELECT goal_id INTO goal_id_result
    FROM Financial_Goals
    WHERE user_id = p_user_id AND goal_name = p_goal_name
    LIMIT 1;
    
    RETURN IFNULL(goal_id_result, -1);
END//

-- ========================================
-- STORED PROCEDURES
-- ========================================

-- Procedure to get all users (or subset)
CREATE PROCEDURE GetUsers(IN p_active_only TINYINT)
BEGIN
    IF p_active_only = 1 THEN
        SELECT user_id, username, email, first_name, last_name, date_created, last_login
        FROM Users 
        WHERE is_active = 1
        ORDER BY username;
    ELSE
        SELECT user_id, username, email, first_name, last_name, date_created, last_login, is_active
        FROM Users 
        ORDER BY username;
    END IF;
END//

-- Procedure to get categories for a user
CREATE PROCEDURE GetCategoriesByUser(IN p_user_id INT)
BEGIN
    SELECT category_id, category_name, category_type, description, color_code, is_active, created_at
    FROM Categories
    WHERE user_id = p_user_id
    ORDER BY category_type, category_name;
END//

-- Procedure to get accounts for a user
CREATE PROCEDURE GetAccountsByUser(IN p_user_id INT)
BEGIN
    SELECT account_id, account_name, account_type, balance, currency, date_created, last_updated, is_active
    FROM Accounts
    WHERE user_id = p_user_id AND is_active = 1
    ORDER BY account_type, account_name;
END//

-- Procedure to get transactions (with pagination)
CREATE PROCEDURE GetTransactions(
    IN p_account_id INT,
    IN p_limit INT,
    IN p_offset INT
)
BEGIN
    IF p_account_id IS NOT NULL THEN
        SELECT t.transaction_id, t.account_id, t.category_id, c.category_name, 
               t.amount, t.description, t.transaction_date, t.transaction_time,
               t.transaction_type, t.status, t.notes, t.created_at
        FROM Transactions t
        JOIN Categories c ON t.category_id = c.category_id
        WHERE t.account_id = p_account_id
        ORDER BY t.transaction_date DESC, t.created_at DESC
        LIMIT p_limit OFFSET p_offset;
    ELSE
        SELECT t.transaction_id, t.account_id, a.account_name, t.category_id, c.category_name, 
               t.amount, t.description, t.transaction_date, t.transaction_time,
               t.transaction_type, t.status, t.notes, t.created_at
        FROM Transactions t
        JOIN Accounts a ON t.account_id = a.account_id
        JOIN Categories c ON t.category_id = c.category_id
        ORDER BY t.transaction_date DESC, t.created_at DESC
        LIMIT p_limit OFFSET p_offset;
    END IF;
END//

-- Procedure to get budgets for a user
CREATE PROCEDURE GetBudgetsByUser(IN p_user_id INT)
BEGIN
    SELECT b.budget_id, b.user_id, b.category_id, c.category_name,
           b.budget_amount, b.spent_amount, b.period_type,
           b.start_date, b.end_date, b.is_active, b.created_at
    FROM Budgets b
    JOIN Categories c ON b.category_id = c.category_id
    WHERE b.user_id = p_user_id
    ORDER BY b.start_date DESC, c.category_name;
END//

-- Procedure to get financial goals for a user
CREATE PROCEDURE GetGoalsByUser(IN p_user_id INT)
BEGIN
    SELECT goal_id, goal_name, target_amount, current_amount, target_date,
           goal_type, priority_level, description, is_completed, 
           created_at, completed_at,
           ROUND((current_amount / target_amount) * 100, 2) as progress_percentage
    FROM Financial_Goals
    WHERE user_id = p_user_id
    ORDER BY priority_level DESC, target_date ASC;
END//

-- Procedure to add a new transaction
CREATE PROCEDURE AddTransaction(
    IN p_account_id INT,
    IN p_category_id INT,
    IN p_amount DECIMAL(10,2),
    IN p_description VARCHAR(255),
    IN p_transaction_date DATE,
    IN p_transaction_time TIME,
    IN p_transaction_type ENUM('income', 'expense', 'transfer'),
    IN p_notes TEXT
)
BEGIN
    DECLARE v_transaction_id INT;
    
    -- Insert new transaction
    INSERT INTO Transactions (
        account_id, category_id, amount, description, 
        transaction_date, transaction_time, transaction_type, 
        status, notes
    ) VALUES (
        p_account_id, p_category_id, p_amount, p_description,
        p_transaction_date, p_transaction_time, p_transaction_type,
        'completed', p_notes
    );
    
    SET v_transaction_id = LAST_INSERT_ID();
    
    -- Update account balance
    IF p_transaction_type = 'income' THEN
        UPDATE Accounts SET balance = balance + p_amount WHERE account_id = p_account_id;
    ELSEIF p_transaction_type = 'expense' THEN
        UPDATE Accounts SET balance = balance + p_amount WHERE account_id = p_account_id;
    END IF;
    
    SELECT 'Transaction added successfully' as message, 
           v_transaction_id as new_transaction_id;
END//

-- Procedure to update a budget (with cascading effects)
CREATE PROCEDURE UpdateBudget(
    IN p_budget_id INT,
    IN p_budget_amount DECIMAL(10,2),
    IN p_period_type ENUM('weekly', 'monthly', 'yearly'),
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    DECLARE v_user_id INT;
    DECLARE v_category_id INT;
    DECLARE v_spent_amount DECIMAL(10,2);
    
    -- Get budget details
    SELECT user_id, category_id INTO v_user_id, v_category_id
    FROM Budgets WHERE budget_id = p_budget_id;
    
    -- Calculate actual spent amount for the new period
    SELECT COALESCE(SUM(ABS(t.amount)), 0) INTO v_spent_amount
    FROM Transactions t
    JOIN Accounts a ON t.account_id = a.account_id
    WHERE a.user_id = v_user_id 
      AND t.category_id = v_category_id
      AND t.transaction_date BETWEEN p_start_date AND p_end_date
      AND t.transaction_type = 'expense'
      AND t.status = 'completed';
    
    -- Update budget
    UPDATE Budgets 
    SET budget_amount = p_budget_amount,
        spent_amount = v_spent_amount,
        period_type = p_period_type,
        start_date = p_start_date,
        end_date = p_end_date
    WHERE budget_id = p_budget_id;
    
    SELECT 'Budget updated successfully' as message, 
           p_budget_id as budget_id, 
           v_spent_amount as recalculated_spent_amount;
END//

-- Procedure to delete a transaction (with cascading effects)
CREATE PROCEDURE DeleteTransaction(IN p_transaction_id INT)
BEGIN
    DECLARE v_account_id INT;
    DECLARE v_amount DECIMAL(10,2);
    DECLARE v_transaction_type ENUM('income', 'expense', 'transfer');
    DECLARE v_account_balance DECIMAL(15,2);
    
    -- Get transaction details
    SELECT account_id, amount, transaction_type 
    INTO v_account_id, v_amount, v_transaction_type
    FROM Transactions 
    WHERE transaction_id = p_transaction_id;
    
    -- Delete related transaction splits first (cascading)
    DELETE FROM Transaction_Splits WHERE transaction_id = p_transaction_id;
    
    -- Delete the transaction
    DELETE FROM Transactions WHERE transaction_id = p_transaction_id;
    
    -- Update account balance (reverse the transaction effect)
    IF v_transaction_type = 'income' THEN
        UPDATE Accounts SET balance = balance - v_amount WHERE account_id = v_account_id;
    ELSEIF v_transaction_type = 'expense' THEN
        UPDATE Accounts SET balance = balance - v_amount WHERE account_id = v_account_id;
    END IF;
    
    SELECT 'Transaction deleted successfully' as message, 
           p_transaction_id as deleted_transaction_id,
           v_account_id as affected_account_id;
END//

DELIMITER ;


-- Initial view of both views
SELECT 'Initial Monthly Expense Summary View:' as section;
SELECT * FROM Monthly_Expense_Summary LIMIT 10;

SELECT 'Initial Budget Performance Analysis View:' as section;
SELECT * FROM Budget_Performance_Analysis;

-- Test all functions
SELECT 'Testing Functions:' as section;
SELECT GetUserIdByUsername('john_doe') as john_user_id;
SELECT GetCategoryIdByName(1, 'Groceries') as groceries_category_id;
SELECT GetAccountIdByName(1, 'Main Checking') as main_checking_id;
SELECT GetBudgetIdByUserCategory(1, 3, '2024-01-01') as budget_id;
SELECT GetGoalIdByName(1, 'Emergency Fund') as goal_id;

-- Test all stored procedures
SELECT 'Testing Get Procedures:' as section;

CALL GetUsers(1);
CALL GetCategoriesByUser(1);
CALL GetAccountsByUser(1);
CALL GetTransactions(1, 5, 0);
CALL GetBudgetsByUser(1);
CALL GetGoalsByUser(1);

-- Test update procedure (changes should cascade)
SELECT 'Testing Update Procedure:' as section;
CALL UpdateBudget(1, 700.00, 'monthly', '2024-01-01', '2024-01-31');

-- Test delete procedure (deletions should cascade)
SELECT 'Testing Delete Procedure:' as section;
CALL DeleteTransaction(1);

-- Final view of both views (should show changes)
SELECT 'Final Monthly Expense Summary View (after changes):' as section;
SELECT * FROM Monthly_Expense_Summary LIMIT 10;

SELECT 'Final Budget Performance Analysis View (after changes):' as section;
SELECT * FROM Budget_Performance_Analysis;
