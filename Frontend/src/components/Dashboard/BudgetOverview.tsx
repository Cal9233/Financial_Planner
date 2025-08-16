import React from 'react';
import {
  Box,
  Typography,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Chip,
} from '@mui/material';
import { Budget } from '../../types';

interface BudgetOverviewProps {
  budgets: Budget[];
}

const BudgetOverview: React.FC<BudgetOverviewProps> = ({ budgets }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Over Budget':
        return 'error';
      case 'Near Limit':
        return 'warning';
      case 'Within Budget':
        return 'success';
      default:
        return 'default';
    }
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 100) return 'error';
    if (percentage >= 80) return 'warning';
    return 'primary';
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Budget Status
      </Typography>
      
      {budgets.length === 0 ? (
        <Typography color="text.secondary" align="center" sx={{ py: 3 }}>
          No active budgets
        </Typography>
      ) : (
        <List dense>
          {budgets.slice(0, 5).map((budget) => (
            <ListItem key={budget.budget_id} sx={{ px: 0 }}>
              <ListItemText
                primary={
                  <Box>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                      <Typography variant="body2">
                        {budget.category_name}
                      </Typography>
                      <Chip
                        label={budget.status}
                        size="small"
                        color={getStatusColor(budget.status || '')}
                      />
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={Math.min(budget.utilization_percentage || 0, 100)}
                      color={getProgressColor(budget.utilization_percentage || 0)}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                }
                secondary={
                  <Box display="flex" justifyContent="space-between" mt={0.5}>
                    <Typography variant="caption" color="text.secondary">
                      ${budget.spent_amount.toFixed(2)} / ${budget.budget_amount.toFixed(2)}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {budget.utilization_percentage?.toFixed(0)}%
                    </Typography>
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

export default BudgetOverview;