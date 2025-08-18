import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Card,
  CardContent,
  CircularProgress,
  Alert,
} from '@mui/material';
import Grid from '@mui/material/Grid';
import {
  TrendingUp,
  TrendingDown,
  AccountBalance,
  Assessment,
} from '@mui/icons-material';
import { format } from 'date-fns';
import api from '../../services/api';
import SpendingChart from './SpendingChart';
import RecentTransactions from './RecentTransactions';
import BudgetOverview from './BudgetOverview';
import GoalProgress from './GoalProgress';

interface DashboardData {
  summary: {
    total_income: number;
    total_expenses: number;
    net_income: number;
    transaction_count: number;
  };
  accounts: any[];
  recentTransactions: any[];
  budgets: any[];
  goals: any[];
}

const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const currentMonth = format(new Date(), 'MMMM yyyy');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [summaryRes, accountsRes, transactionsRes, budgetsRes, goalsRes] = await Promise.all([
        api.get('/api/dashboard/summary'),
        api.get('/api/accounts'),
        api.get('/api/dashboard/recent-transactions'),
        api.get('/api/budgets'),
        api.get('/api/goals'),
      ]);

      setData({
        summary: summaryRes.data,
        accounts: accountsRes.data.accounts || [],
        recentTransactions: transactionsRes.data.transactions || [],
        budgets: budgetsRes.data.budgets || [],
        goals: goalsRes.data.goals || [],
      });
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  if (!data) return null;

  const totalBalance = data.accounts.reduce((sum, acc) => sum + acc.balance, 0);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        {currentMonth} Overview
      </Typography>

      <Grid container spacing={3}>
        {/* Summary Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Total Income
                  </Typography>
                  <Typography variant="h5" color="success.main">
                    ${data.summary.total_income.toFixed(2)}
                  </Typography>
                </Box>
                <TrendingUp color="success" fontSize="large" />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Total Expenses
                  </Typography>
                  <Typography variant="h5" color="error.main">
                    ${data.summary.total_expenses.toFixed(2)}
                  </Typography>
                </Box>
                <TrendingDown color="error" fontSize="large" />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Net Income
                  </Typography>
                  <Typography 
                    variant="h5" 
                    color={data.summary.net_income >= 0 ? 'success.main' : 'error.main'}
                  >
                    ${data.summary.net_income.toFixed(2)}
                  </Typography>
                </Box>
                <Assessment color="primary" fontSize="large" />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Total Balance
                  </Typography>
                  <Typography variant="h5" color="primary.main">
                    ${totalBalance.toFixed(2)}
                  </Typography>
                </Box>
                <AccountBalance color="primary" fontSize="large" />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Spending Chart */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <SpendingChart />
          </Paper>
        </Grid>

        {/* Budget Overview */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <BudgetOverview budgets={data.budgets} />
          </Paper>
        </Grid>

        {/* Recent Transactions */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <RecentTransactions transactions={data.recentTransactions} />
          </Paper>
        </Grid>

        {/* Goal Progress */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <GoalProgress goals={data.goals} />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;