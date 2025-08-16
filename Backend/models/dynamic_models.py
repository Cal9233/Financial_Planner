"""Dynamic model loading for runtime database connections"""
from sqlalchemy import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from config.dynamic_config import get_dynamic_db, engine

# Cache for loaded models
_model_cache = {}

def get_model(model_name):
    """Get a model class dynamically based on current database connection"""
    
    # Check cache first
    if model_name in _model_cache:
        return _model_cache[model_name]
    
    # Import the model class
    if model_name == 'User':
        from .user import User
        _model_cache[model_name] = User
        return User
    elif model_name == 'Category':
        from .category import Category
        _model_cache[model_name] = Category
        return Category
    elif model_name == 'Account':
        from .account import Account
        _model_cache[model_name] = Account
        return Account
    elif model_name == 'Transaction':
        from .transaction import Transaction
        _model_cache[model_name] = Transaction
        return Transaction
    elif model_name == 'TransactionSplit':
        from .transaction import TransactionSplit
        _model_cache[model_name] = TransactionSplit
        return TransactionSplit
    elif model_name == 'Budget':
        from .budget import Budget
        _model_cache[model_name] = Budget
        return Budget
    elif model_name == 'FinancialGoal':
        from .goal import FinancialGoal
        _model_cache[model_name] = FinancialGoal
        return FinancialGoal
    else:
        raise ValueError(f"Unknown model: {model_name}")

def clear_model_cache():
    """Clear the model cache (useful when changing databases)"""
    global _model_cache
    _model_cache = {}