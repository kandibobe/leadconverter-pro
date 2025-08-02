import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth.store';
// ... (импорты компонентов)
import LoginView from '@/views/LoginView.vue';
import SettingsView from '@/views/admin/SettingsView.vue';

const routes = [
  { path: '/', name: 'Quiz', component: QuizView },
  { path: '/login', name: 'Login', component: LoginView },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Dashboard', component: DashboardView },
      { path: 'leads', name: 'AdminLeads', component: LeadsView },
      { path: 'settings', name: 'AdminSettings', component: SettingsView },
    ],
  },
];

const router = createRouter({ /* ... */ });

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;