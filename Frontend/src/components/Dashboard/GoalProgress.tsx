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
import { format } from 'date-fns';
import { FinancialGoal } from '../../types';

interface GoalProgressProps {
  goals: FinancialGoal[];
}

const GoalProgress: React.FC<GoalProgressProps> = ({ goals }) => {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Financial Goals
      </Typography>
      
      {goals.length === 0 ? (
        <Typography color="text.secondary" align="center" sx={{ py: 3 }}>
          No active goals
        </Typography>
      ) : (
        <List dense>
          {goals.slice(0, 5).map((goal) => (
            <ListItem key={goal.goal_id} sx={{ px: 0 }}>
              <ListItemText
                primary={
                  <Box>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                      <Typography variant="body2">
                        {goal.goal_name}
                      </Typography>
                      <Chip
                        label={goal.priority_level}
                        size="small"
                        color={getPriorityColor(goal.priority_level)}
                      />
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={goal.progress_percentage || 0}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                }
                secondary={
                  <Box display="flex" justifyContent="space-between" mt={0.5}>
                    <Typography variant="caption" color="text.secondary">
                      ${goal.current_amount.toFixed(2)} / ${goal.target_amount.toFixed(2)}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {goal.target_date 
                        ? `Due: ${format(new Date(goal.target_date), 'MMM yyyy')}`
                        : 'No deadline'
                      }
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

export default GoalProgress;