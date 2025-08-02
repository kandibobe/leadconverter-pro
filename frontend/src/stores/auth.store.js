import { defineStore } from 'pinia';
import apiClient from '@/services/apiClient';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(email, password) {
      try {
        const params = new URLSearchParams();
        params.append('username', email);
        params.append('password', password);

        const response = await apiClient.post('/login/access-token', params, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
        
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token);
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        this.error = null;
        router.push('/admin');
      } catch (err) {
        this.error = 'Неверный email или пароль.';
        console.error(err);
      }
    },
    logout() {
      this.token = null;
      localStorage.removeItem('token');
      delete apiClient.defaults.headers.common['Authorization'];
      router.push('/login');
    },
  },
});