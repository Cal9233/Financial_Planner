# Personal Finance Management System - Frontend

## Phase 3: React Frontend Implementation

This is the React frontend for the Personal Finance Management System. It provides a modern, responsive interface for managing personal finances.

## Features Implemented

### 1. **Database Connection Flow**
- Initial database connection screen
- Secure credential input with validation
- Connection testing before proceeding

### 2. **Authentication**
- User registration with form validation
- Login with JWT token management
- Automatic token refresh
- Protected routes

### 3. **Dashboard**
- Monthly income/expense summary cards
- Account balance overview
- Spending chart (pie chart)
- Recent transactions list
- Budget performance overview
- Goal progress tracking

### 4. **Transaction Management**
- Full CRUD operations
- Advanced filtering (by account, category, type)
- Pagination
- Search functionality
- Form validation

### 5. **UI/UX Features**
- Material-UI components for consistent design
- Responsive layout that works on mobile and desktop
- Loading states and error handling
- Clean, modern interface

## Setup Instructions

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Configure API URL** (optional)
   - Create a `.env` file in the frontend directory
   - Add: `REACT_APP_API_URL=http://localhost:5000`

3. **Start Development Server**
   ```bash
   npm start
   ```

The app will open at http://localhost:3000

## Available Scripts

- `npm start` - Runs the development server
- `npm build` - Creates production build
- `npm test` - Runs tests
- `npm eject` - Ejects from Create React App (not recommended)

## Application Flow

1. **Database Connection**: Users must first connect to their MySQL database
2. **Authentication**: Register or login to access the application
3. **Dashboard**: View financial overview and key metrics
4. **Navigation**: Use the sidebar to access different features

## Technologies Used

- React 18 with TypeScript
- Material-UI for components
- React Router for navigation
- Axios for API calls
- Chart.js for data visualization
- date-fns for date formatting

## Project Structure

```
src/
├── components/
│   ├── Auth/           # Authentication components
│   ├── Dashboard/      # Dashboard and widgets
│   ├── Transactions/   # Transaction management
│   ├── Common/         # Shared components
│   └── ...            # Other feature components
├── contexts/          # React contexts
├── services/          # API services
├── types/             # TypeScript types
└── App.tsx           # Main app component
```

## Next Steps

The following components are scaffolded and ready for implementation:
- Account management
- Budget creation and tracking
- Financial goal management
- Report generation with PDF export

## Security Notes

- Database credentials are stored in secure sessions
- JWT tokens are used for API authentication
- Automatic logout on token expiration
- CORS configured for API communication