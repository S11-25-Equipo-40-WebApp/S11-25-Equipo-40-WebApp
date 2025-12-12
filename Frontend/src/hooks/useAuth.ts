import { useCallback } from 'react';

export const useAuth = () => {
  const getAuthHeaders = useCallback(() => {
    const token = typeof window !== 'undefined' ? localStorage?.getItem('token') : null;
    return {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };
  }, []);

  return { getAuthHeaders };
};
