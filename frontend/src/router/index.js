// /frontend/src/router/index.js (ФИНАЛЬНАЯ ИСПРАВЛЕННАЯ ВЕРСИЯ)

import { createRouter, createWebHistory } from 'vue-router';

// Используем ТОЛЬКО надежные алиасы '@'
import QuizView from '@/views/QuizView.vue';
import CheckoutView from '@/views/CheckoutView.vue';
import AdminLayout from '@/layouts/AdminLayout.vue';
import DashboardView from '@/views/admin/DashboardView.vue';
import LeadsView from '@/views/admin/LeadsView.vue'; // Добавим страницу лидов
import BillingView from '@/views/admin/BillingView.vue';

const routes = [
  // --- Клиентская часть ---
  {
    path: '/',
    name: 'Quiz',
    component: QuizView
  },
  {
    path: '/subscribe',
    name: 'Checkout',
    component: CheckoutView
  },

  // --- Админ-панель ---
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: '', // Дашборд по адресу /admin
        name: 'Dashboard',
        component: DashboardView
      },
      {
        path: 'leads', // Страница лидов по адресу /admin/leads
        name: 'AdminLeads',
        component: LeadsView
      },
      {
        path: 'billing',
        name: 'AdminBilling',
        component: BillingView
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;