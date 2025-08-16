from .auth import auth_bp
from .users import users_bp
from .categories import categories_bp
from .accounts import accounts_bp
from .transactions import transactions_bp
from .budgets import budgets_bp
from .goals import goals_bp
from .reports import reports_bp

__all__ = [
    'auth_bp',
    'users_bp',
    'categories_bp',
    'accounts_bp',
    'transactions_bp',
    'budgets_bp',
    'goals_bp',
    'reports_bp'
]