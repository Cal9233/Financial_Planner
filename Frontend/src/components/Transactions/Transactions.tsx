import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  MenuItem,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  InputAdornment,
} from '@mui/material';
import Grid from '@mui/material/Grid';
import {
  Add,
  Edit,
  Delete,
  FilterList,
  Search,
} from '@mui/icons-material';
import { format } from 'date-fns';
import api from '../../services/api';
import { Transaction, Account, Category } from '../../types';

// Define transaction type union
type TransactionType = 'expense' | 'income' | 'transfer';

const Transactions: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [total, setTotal] = useState(0);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingTransaction, setEditingTransaction] = useState<Transaction | null>(null);
  const [filters, setFilters] = useState({
    account_id: '',
    category_id: '',
    type: '',
    search: '',
  });

  const [formData, setFormData] = useState({
    account_id: '',
    category_id: '',
    amount: '',
    description: '',
    transaction_date: format(new Date(), 'yyyy-MM-dd'),
    transaction_type: 'expense' as TransactionType, // Fix: Use the union type
    notes: '',
  });

  useEffect(() => {
    loadData();
  }, [page, rowsPerPage, filters]);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Load accounts and categories once
      if (accounts.length === 0 || categories.length === 0) {
        const [accountsRes, categoriesRes] = await Promise.all([
          api.get('/api/accounts'),
          api.get('/api/categories'),
        ]);
        setAccounts(accountsRes.data.accounts);
        setCategories(categoriesRes.data.categories);
      }

      // Load transactions with filters
      const params = new URLSearchParams({
        page: (page + 1).toString(),
        per_page: rowsPerPage.toString(),
        ...(filters.account_id && { account_id: filters.account_id }),
        ...(filters.category_id && { category_id: filters.category_id }),
        ...(filters.type && { type: filters.type }),
      });

      const response = await api.get(`/api/transactions?${params}`);
      setTransactions(response.data.transactions);
      setTotal(response.data.total);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (transaction?: Transaction) => {
    if (transaction) {
      setEditingTransaction(transaction);
      setFormData({
        account_id: transaction.account_id.toString(),
        category_id: transaction.category_id.toString(),
        amount: Math.abs(transaction.amount).toString(),
        description: transaction.description || '',
        transaction_date: transaction.transaction_date,
        transaction_type: transaction.transaction_type as TransactionType, // Fix: Cast to union type
        notes: transaction.notes || '',
      });
    } else {
      setEditingTransaction(null);
      setFormData({
        account_id: '',
        category_id: '',
        amount: '',
        description: '',
        transaction_date: format(new Date(), 'yyyy-MM-dd'),
        transaction_type: 'expense',
        notes: '',
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingTransaction(null);
  };

  const handleSubmit = async () => {
    try {
      const data = {
        ...formData,
        account_id: parseInt(formData.account_id),
        category_id: parseInt(formData.category_id),
        amount: parseFloat(formData.amount),
      };

      if (editingTransaction) {
        await api.put(`/api/transactions/${editingTransaction.transaction_id}`, data);
      } else {
        await api.post('/api/transactions', data);
      }

      handleCloseDialog();
      loadData();
    } catch (error) {
      console.error('Failed to save transaction:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this transaction?')) {
      try {
        await api.delete(`/api/transactions/${id}`);
        loadData();
      } catch (error) {
        console.error('Failed to delete transaction:', error);
      }
    }
  };

  const getTransactionColor = (type: string) => {
    switch (type) {
      case 'income':
        return 'success';
      case 'expense':
        return 'error';
      case 'transfer':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Transactions</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Add Transaction
        </Button>
      </Box>

      {/* Filters */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={3}>
            <TextField
              select
              fullWidth
              label="Account"
              value={filters.account_id}
              onChange={(e) => setFilters({ ...filters, account_id: e.target.value })}
              size="small"
            >
              <MenuItem value="">All Accounts</MenuItem>
              {accounts.map((account) => (
                <MenuItem key={account.account_id} value={account.account_id}>
                  {account.account_name}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              select
              fullWidth
              label="Category"
              value={filters.category_id}
              onChange={(e) => setFilters({ ...filters, category_id: e.target.value })}
              size="small"
            >
              <MenuItem value="">All Categories</MenuItem>
              {categories.map((category) => (
                <MenuItem key={category.category_id} value={category.category_id}>
                  {category.category_name}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              select
              fullWidth
              label="Type"
              value={filters.type}
              onChange={(e) => setFilters({ ...filters, type: e.target.value })}
              size="small"
            >
              <MenuItem value="">All Types</MenuItem>
              <MenuItem value="income">Income</MenuItem>
              <MenuItem value="expense">Expense</MenuItem>
              <MenuItem value="transfer">Transfer</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              fullWidth
              label="Search"
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              size="small"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
        </Grid>
      </Paper>

      {/* Transactions Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Account</TableCell>
              <TableCell>Type</TableCell>
              <TableCell align="right">Amount</TableCell>
              <TableCell align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transactions.map((transaction) => (
              <TableRow key={transaction.transaction_id}>
                <TableCell>
                  {format(new Date(transaction.transaction_date), 'MMM dd, yyyy')}
                </TableCell>
                <TableCell>{transaction.description || '-'}</TableCell>
                <TableCell>{transaction.category_name}</TableCell>
                <TableCell>{transaction.account_name}</TableCell>
                <TableCell>
                  <Chip
                    label={transaction.transaction_type}
                    size="small"
                    color={getTransactionColor(transaction.transaction_type)}
                  />
                </TableCell>
                <TableCell align="right">
                  <Typography
                    color={transaction.transaction_type === 'expense' ? 'error' : 'success'}
                  >
                    {transaction.transaction_type === 'expense' ? '-' : '+'}
                    ${Math.abs(transaction.amount).toFixed(2)}
                  </Typography>
                </TableCell>
                <TableCell align="center">
                  <IconButton
                    size="small"
                    onClick={() => handleOpenDialog(transaction)}
                  >
                    <Edit />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(transaction.transaction_id)}
                    color="error"
                  >
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <TablePagination
          component="div"
          count={total}
          page={page}
          onPageChange={(_, newPage) => setPage(newPage)}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={(e) => {
            setRowsPerPage(parseInt(e.target.value, 10));
            setPage(0);
          }}
        />
      </TableContainer>

      {/* Add/Edit Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingTransaction ? 'Edit Transaction' : 'Add Transaction'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                label="Account"
                value={formData.account_id}
                onChange={(e) => setFormData({ ...formData, account_id: e.target.value })}
                required
              >
                {accounts.map((account) => (
                  <MenuItem key={account.account_id} value={account.account_id}>
                    {account.account_name}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                label="Category"
                value={formData.category_id}
                onChange={(e) => setFormData({ ...formData, category_id: e.target.value })}
                required
              >
                {categories
                  .filter((cat) => {
                    // Fix: Proper type checking for category filtering
                    return cat.category_type === formData.transaction_type || formData.transaction_type === 'transfer';
                  })
                  .map((category) => (
                    <MenuItem key={category.category_id} value={category.category_id}>
                      {category.category_name}
                    </MenuItem>
                  ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                select
                fullWidth
                label="Type"
                value={formData.transaction_type}
                onChange={(e) => setFormData({ ...formData, transaction_type: e.target.value as TransactionType })} // Fix: Cast to union type
              >
                <MenuItem value="income">Income</MenuItem>
                <MenuItem value="expense">Expense</MenuItem>
                <MenuItem value="transfer">Transfer</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Amount"
                type="number"
                value={formData.amount}
                onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                required
                InputProps={{
                  startAdornment: <InputAdornment position="start">$</InputAdornment>,
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Date"
                type="date"
                value={formData.transaction_date}
                onChange={(e) => setFormData({ ...formData, transaction_date: e.target.value })}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Notes"
                multiline
                rows={3}
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingTransaction ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Transactions;