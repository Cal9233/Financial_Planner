import React from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Chip,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  SwapHoriz,
} from '@mui/icons-material';
import { format } from 'date-fns';
import { Transaction } from '../../types';

interface RecentTransactionsProps {
  transactions: Transaction[];
}

const RecentTransactions: React.FC<RecentTransactionsProps> = ({ transactions }) => {
  const getTransactionIcon = (type: string) => {
    switch (type) {
      case 'income':
        return <TrendingUp />;
      case 'expense':
        return <TrendingDown />;
      case 'transfer':
        return <SwapHoriz />;
      default:
        return <TrendingDown />;
    }
  };

  const getTransactionColor = (type: string) => {
    switch (type) {
      case 'income':
        return 'success.main';
      case 'expense':
        return 'error.main';
      case 'transfer':
        return 'info.main';
      default:
        return 'text.primary';
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Recent Transactions
      </Typography>
      
      {transactions.length === 0 ? (
        <Typography color="text.secondary" align="center" sx={{ py: 3 }}>
          No transactions yet
        </Typography>
      ) : (
        <List>
          {transactions.map((transaction) => (
            <ListItem key={transaction.transaction_id} divider>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: getTransactionColor(transaction.transaction_type) }}>
                  {getTransactionIcon(transaction.transaction_type)}
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="body1">
                      {transaction.description || transaction.category_name}
                    </Typography>
                    <Typography
                      variant="body1"
                      fontWeight="bold"
                      color={getTransactionColor(transaction.transaction_type)}
                    >
                      {transaction.transaction_type === 'expense' ? '-' : '+'}
                      ${Math.abs(transaction.amount).toFixed(2)}
                    </Typography>
                  </Box>
                }
                secondary={
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="caption" color="text.secondary">
                      {format(new Date(transaction.transaction_date), 'MMM dd, yyyy')}
                    </Typography>
                    <Chip
                      label={transaction.category_name}
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );
};

export default RecentTransactions;