from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils.db_manager import DatabaseManager

# Global database instance
db = None
engine = None
db_session = None

def init_dynamic_db(app):
    """Initialize database with dynamic connection"""
    global db, engine, db_session
    
    if not db:
        db = SQLAlchemy()
    
    # Check if we have connection info in session
    conn_info = DatabaseManager.get_connection_info()
    
    if conn_info:
        # Create connection string from session data
        conn_string = DatabaseManager.create_connection_string(
            host=conn_info['host'],
            user=conn_info['user'],
            password=conn_info['password'],
            database=conn_info['database'],
            port=conn_info.get('port', 3306)
        )
        
        # Update app config
        app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
        
        # Initialize database
        db.init_app(app)
        
        # Create engine and session
        engine = create_engine(conn_string)
        db_session = scoped_session(sessionmaker(bind=engine))
        
        return True
    
    return False

def get_dynamic_db():
    """Get the current database instance"""
    global db
    return db

def get_db_session():
    """Get the current database session"""
    global db_session
    return db_session

def close_db_session():
    """Close the database session"""
    global db_session
    if db_session:
        db_session.remove()