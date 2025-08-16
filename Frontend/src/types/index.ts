export interface User {
  user_id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  date_created: string;
  last_login: string | null;
  is_active: boolean;
}

export interface Category {
  category_id: number;
  user_id: number;
  category_name: string;
  category_type: 'income' | 'expense';
  description: string | null;
  color_code: string | null;
  is_active: boolean;
  created_at: string;
}

export interface Account {
  account_id: number;
  user_id: number;
  account_name: string;
  account_type: 'checking' | 'savings' | 'credit' | 'investment';
  balance: number;
  currency: string;
  date_created: string;
  last_updated: string;
  is_active: boolean;
}

export interface Transaction {
  transaction_id: number;
  account_id: number;
  category_id: number;
  category_name?: string;
  account_name?: string;
  amount: number;
  description: string | null;
  transaction_date: string;
  transaction_time: string;
  transaction_type: 'income' | 'expense' | 'transfer';
  status: 'pending' | 'completed' | 'cancelled';
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface Budget {
  budget_id: number;
  user_id: number;
  category_id: number;
  category_name?: string;
  budget_amount: number;
  spent_amount: number;
  period_type: 'weekly' | 'monthly' | 'yearly';
  start_date: string;
  end_date: string;
  is_active: boolean;
  created_at: string;
  utilization_percentage?: number;
  remaining_budget?: number;
  status?: 'Over Budget' | 'Near Limit' | 'Within Budget';
}

export interface FinancialGoal {
  goal_id: number;
  user_id: number;
  goal_name: string;
  target_amount: number;
  current_amount: number;
  target_date: string | null;
  goal_type: 'savings' | 'debt_payoff' | 'investment';
  priority_level: 'low' | 'medium' | 'high';
  description: string | null;
  is_completed: boolean;
  created_at: string;
  completed_at: string | null;
  progress_percentage?: number;
}

export interface DatabaseConfig {
  host: string;
  user: string;
  password: string;
  database: string;
  port?: number;
}

export interface AuthResponse {
  message: string;
  user: User;
  access_token: string;
  refresh_token: string;
}

export interface DatabaseStatus {
  connected: boolean;
  database?: string;
  host?: string;
  user?: string;
}