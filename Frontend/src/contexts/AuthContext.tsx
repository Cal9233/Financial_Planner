import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import api from '../services/api';
import { User, DatabaseStatus } from '../types';

interface AuthContextType {
  user: User | null;
  dbStatus: DatabaseStatus;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (userData: any) => Promise<void>;
  logout: () => Promise<void>;
  connectDatabase: (credentials: any) => Promise<any>;
  disconnectDatabase: () => Promise<void>;
  checkDatabaseStatus: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [dbStatus, setDbStatus] = useState<DatabaseStatus>({ connected: false });
  const [isLoading, setIsLoading] = useState(true);

  const checkDatabaseStatus = async () => {
    try {
      const response = await api.get('/api/database/status');
      setDbStatus(response.data);
    } catch (error) {
      console.error('Failed to check database status:', error);
      setDbStatus({ connected: false });
    }
  };

  const connectDatabase = async (credentials: any) => {
    const response = await api.post('/api/database/connect', credentials);
    if (response.data.connected) {
      setDbStatus(response.data);
    }
    return response.data;
  };

  const disconnectDatabase = async () => {
    await api.post('/api/database/disconnect');
    setDbStatus({ connected: false });
    setUser(null);
    localStorage.clear();
  };

  const login = async (username: string, password: string) => {
    const response = await api.post('/api/auth/login', { username, password });
    const { user, access_token, refresh_token } = response.data;
    
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    setUser(user);
  };

  const register = async (userData: any) => {
    const response = await api.post('/api/auth/register', userData);
    const { user, access_token, refresh_token } = response.data;
    
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    setUser(user);
  };

  const logout = async () => {
    try {
      await api.post('/api/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    }
    
    setUser(null);
    localStorage.clear();
  };

  const loadUserProfile = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setIsLoading(false);
        return;
      }

      const response = await api.get('/api/users/profile');
      setUser(response.data.user);
    } catch (error: any) {
      console.error('Failed to load user profile:', error);
      // Only clear storage if it's a 401 error
      if (error.response?.status === 401) {
        localStorage.clear();
        setUser(null);
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const initialize = async () => {
      await checkDatabaseStatus();
      await loadUserProfile();
    };
    initialize();
  }, []);

  const value = {
    user,
    dbStatus,
    isLoading,
    login,
    register,
    logout,
    connectDatabase,
    disconnectDatabase,
    checkDatabaseStatus,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};