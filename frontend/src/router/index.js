// /frontend/src/router/index.js (ФИНАЛЬНАЯ ИСПРАВЛЕННАЯ ВЕРСИЯ)

import { createRouter, createWebHistory } from 'vue-router';

// Используем ТОЛЬКО надежные алиасы '@'
import QuizView from '@/views/QuizView.vue';
import AdminLayout from '@/layouts/AdminLayout.vue';
import DashboardView from '@/views/admin/DashboardView.vue';
import LeadsView from '@/views/admin/LeadsView.vue'; // Добавим страницу лидов
import HistoryView from '@/views/admin/HistoryView.vue';

const routes = [
  // --- Клиентская часть ---
  {
    path: '/',
    name: 'Quiz',
    component: QuizView
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
        path: 'history',
        name: 'History',
        component: HistoryView
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
