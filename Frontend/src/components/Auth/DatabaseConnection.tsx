import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  IconButton,
  InputAdornment,
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';

const DatabaseConnection: React.FC = () => {
  const { connectDatabase, checkDatabaseStatus, dbStatus } = useAuth();
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({
    host: 'localhost',
    user: '',
    password: '',
    database: 'personal_finance_db',
    port: 3306,
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // If already connected, redirect to login
    if (dbStatus.connected) {
      navigate('/login');
    }
  }, [dbStatus.connected, navigate]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: name === 'port' ? parseInt(value) || 3306 : value,
    }));
    setError('');
  };

  const handleConnect = async () => {
    setLoading(true);
    setError('');

    try {
      const result = await connectDatabase(credentials);
      if (result.connected) {
        // Update the database status in context
        await checkDatabaseStatus();
        // Redirect to login page
        navigate('/login');
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to connect to database');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
      bgcolor="background.default"
    >
      <Card sx={{ maxWidth: 500, width: '100%', mx: 2 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom align="center">
            Connect to MySQL Database
          </Typography>
          
          <Typography variant="body2" color="text.secondary" paragraph>
            Enter your MySQL database credentials to connect to your personal finance database.
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              name="host"
              label="Host"
              value={credentials.host}
              onChange={handleChange}
              disabled={loading}
            />
            
            <TextField
              margin="normal"
              required
              fullWidth
              name="user"
              label="Username"
              value={credentials.user}
              onChange={handleChange}
              disabled={loading}
            />
            
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type={showPassword ? 'text' : 'password'}
              value={credentials.password}
              onChange={handleChange}
              disabled={loading}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
            
            <TextField
              margin="normal"
              required
              fullWidth
              name="database"
              label="Database Name"
              value={credentials.database}
              onChange={handleChange}
              disabled={loading}
            />
            
            <TextField
              margin="normal"
              fullWidth
              name="port"
              label="Port"
              type="number"
              value={credentials.port}
              onChange={handleChange}
              disabled={loading}
            />

            <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
              <Button
                fullWidth
                variant="contained"
                onClick={handleConnect}
                disabled={loading || !credentials.user || !credentials.password}
              >
                {loading ? <CircularProgress size={24} /> : 'Connect'}
              </Button>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DatabaseConnection;