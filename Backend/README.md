# Simple Backend Implementation

This is a simplified version of the backend that uses the same approach as DAL.py with direct mysql.connector instead of SQLAlchemy.

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the simple backend:
```bash
python simple_app.py
```

## Key Differences from Original Backend

1. **Direct MySQL Connection**: Uses `mysql.connector` directly instead of SQLAlchemy ORM
2. **Simple Models**: Models use plain Python classes with methods instead of SQLAlchemy models
3. **No Complex Configuration**: No dynamic SQLAlchemy configuration issues
4. **Session-based DB Config**: Database credentials stored in Flask session

## API Endpoints

### Database Connection
- `POST /api/database/connect` - Connect to MySQL database
- `POST /api/database/disconnect` - Disconnect from database
- `GET /api/database/status` - Check connection status
- `POST /api/database/test` - Test database connection

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh JWT token
- `GET /api/auth/me` - Get current user info

## File Structure

```
Backend/
├── simple_app.py              # Main application file
├── config/
│   └── simple_db.py          # Database connection manager
├── models/
│   └── simple_user.py        # User model
└── routes/
    ├── simple_database.py    # Database routes
    └── simple_auth.py        # Authentication routes
```

## Usage Example

1. First connect to database:
```javascript
fetch('http://localhost:5000/api/database/connect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
        host: 'localhost',
        user: 'your_user',
        password: 'your_password',
        database: 'personal_finance_db',
        port: 3306
    })
})
```

2. Then register/login:
```javascript
fetch('http://localhost:5000/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123',
        first_name: 'Test',
        last_name: 'User'
    })
})
```

## Benefits

1. **Simpler**: No complex ORM configuration
2. **More Control**: Direct SQL queries when needed
3. **Easier Debugging**: Clearer error messages
4. **Familiar Pattern**: Similar to DAL.py approach