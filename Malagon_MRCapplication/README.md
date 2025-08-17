# Marine Rental Company (MRC) Management System

## Overview

A complete **GUI application** for managing a marine rental company's operations. This system features vessel management, passenger tracking, trip scheduling, and revenue reporting with a modern graphical user interface built using Python Tkinter.

## 🏗️ Architecture

- **GUI Layer** (GUI.py): Modern Tkinter-based graphical user interface
- **Business Logic Layer** (BLL.py): Manages business rules, validation, and double-booking prevention
- **Data Access Layer** (DAL.py): Handles direct database operations
- **Main Entry Point** (Main.py): Application launcher with dependency checking

## 📋 Prerequisites

1. **Python 3.7 or higher**
2. **MySQL Server** running with the MRC database set up
3. **Required Python packages:**
   ```bash
   pip install mysql-connector-python tkcalendar
   ```

## 💾 Database Setup

1. **Create the database** using the provided SQL script (from your schema file):
   - Run the complete SQL script in your MySQL environment
   - This creates the `mrc` database with all tables, views, functions, and procedures
   - Sample data will be inserted automatically

2. **Verify the database** contains:
   - Tables: `vessels`, `passengers`, `trips`
   - Views: `all trips`, `total revenue by vessel`
   - Functions: `getVesselID`, `getPassengerID`
   - Procedures: `addTrip`, `addVessel`, `addPassenger`, `deleteVessel`, `deletePassenger`

## 📁 File Structure

```
MRC_Project/
├── Main.py             # Application entry point
├── GUI.py              # Graphical User Interface
├── BLL.py              # Business Logic Layer
├── DAL.py              # Data Access Layer
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### Method 1: Using requirements.txt (Recommended)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python Main.py
```

### Method 2: Manual Installation

```bash
# 1. Install packages individually
pip install mysql-connector-python
pip install tkcalendar

# 2. Run the application
python Main.py
```

## 🖥️ Application Features

### **Login Screen**
- Clean, modern login interface
- Database connection with custom credentials
- Input validation and error handling

### **Main Dashboard**
- **📋 View All Trips**: Complete trip listings with passenger and vessel details
- **💰 View Revenue by Vessel**: Financial reports and revenue analysis
- **👥 Manage Passengers**: Add, view, and delete passenger records
- **🚢 Manage Vessels**: Add, view, and delete vessel records
- **➕ Add New Trip**: Schedule new trips with conflict detection
- **🚪 Logout**: Secure session management

### **Key Features**
- **Double Booking Prevention**: Automatically detects and prevents scheduling conflicts
- **Interactive Date/Time Pickers**: User-friendly date and time selection
- **Dropdown Menus**: Easy selection of existing vessels and passengers
- **Data Validation**: Input validation with helpful error messages
- **Modern UI**: Professional styling with consistent color scheme
- **Real-time Updates**: Automatic refresh of data displays

## 🎯 Using the Application

### **First Time Setup**

1. **Launch the application:**
   ```bash
   python Main.py
   ```

2. **Login with your database credentials:**
   - Host: localhost (default)
   - Username: your MySQL username
   - Password: your MySQL password
   - Database: mrc (default)

### **Adding Data**

1. **Add Vessels**: Use "Manage Vessels" → "Add Vessel"
2. **Add Passengers**: Use "Manage Passengers" → "Add Passenger"
3. **Schedule Trips**: Use "Add New Trip" with automatic conflict checking

### **Viewing Reports**

- **All Trips**: Complete history with costs and passenger details
- **Revenue by Vessel**: Financial performance analysis

## ⚠️ Important Features

### **Double Booking Prevention**
The system automatically prevents:
- Same vessel being booked for overlapping times
- Same passenger being double-booked
- Uses actual trip lengths from the database for accurate conflict detection

### **Data Validation**
- Required field validation
- Format checking (phone numbers, costs, etc.)
- Business rule enforcement (positive values, reasonable ranges)