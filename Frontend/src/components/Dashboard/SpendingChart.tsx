import React, { useEffect, useState } from 'react';
import { Box, Typography } from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import api from '../../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const SpendingChart: React.FC = () => {
  const [chartData, setChartData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadChartData();
  }, []);

  const loadChartData = async () => {
    try {
      const response = await api.get('/api/reports/monthly/' + 
        new Date().getFullYear() + '/' + 
        (new Date().getMonth() + 1)
      );
      
      const { category_breakdown } = response.data;
      
      // Prepare data for pie chart
      const expenseCategories = Object.entries(category_breakdown)
        .filter(([_, data]: any) => data.type === 'expense')
        .sort((a: any, b: any) => b[1].total - a[1].total)
        .slice(0, 6); // Top 6 categories

      const labels = expenseCategories.map(([name]) => name);
      const data = expenseCategories.map(([_, catData]: any) => catData.total);
      
      const backgroundColors = [
        '#FF6384',
        '#36A2EB',
        '#FFCE56',
        '#4BC0C0',
        '#9966FF',
        '#FF9F40',
      ];

      setChartData({
        labels,
        datasets: [
          {
            label: 'Spending by Category',
            data,
            backgroundColor: backgroundColors,
            borderWidth: 1,
          },
        ],
      });
    } catch (error) {
      console.error('Failed to load chart data:', error);
    } finally {
      setLoading(false);
    }
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right' as const,
      },
      title: {
        display: true,
        text: 'Expense Categories',
      },
    },
  };

  if (loading || !chartData) {
    return (
      <Box height={300} display="flex" alignItems="center" justifyContent="center">
        <Typography color="text.secondary">Loading chart...</Typography>
      </Box>
    );
  }

  return (
    <Box height={300}>
      <Pie data={chartData} options={options} />
    </Box>
  );
};

export default SpendingChart;