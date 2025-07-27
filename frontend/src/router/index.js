 codex/improve-error-handling-and-add-i18n-support
import { createRouter, createWebHistory } from 'vue-router';

import QuizView from '@/views/QuizView.vue';
import AdminLayout from '@/layouts/AdminLayout.vue';
import DashboardView from '@/views/admin/DashboardView.vue';
import LeadsView from '@/views/admin/LeadsView.vue';

// /frontend/src/router/index.js (ФИНАЛЬНАЯ ИСПРАВЛЕННАЯ ВЕРСИЯ)

import { createRouter, createWebHistory } from 'vue-router';

// Используем ТОЛЬКО надежные алиасы '@'
import QuizView from '@/views/QuizView.vue';
import AdminLayout from '@/layouts/AdminLayout.vue';
import DashboardView from '@/views/admin/DashboardView.vue';
import LeadsView from '@/views/admin/LeadsView.vue'; // Добавим страницу лидов
 main

const routes = [
  // --- Клиентская часть ---
  {
    path: '/',
    name: 'Quiz',
    component: QuizView,
  },

  // --- Админ-панель ---
  {
    path: '/admin',
    component: AdminLayout,
    children: [
 codex/improve-error-handling-and-add-i18n-support
      { path: '', name: 'Dashboard', component: DashboardView },
      { path: 'leads', name: 'Leads', component: LeadsView },
    ],
  },

      {
        path: '', // Дашборд по адресу /admin
        name: 'Dashboard',
        component: DashboardView
      },
      {
        path: 'leads', // Страница лидов по адресу /admin/leads
        name: 'AdminLeads',
        component: LeadsView
      }
    ]
  }
 main
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

 codex/improve-error-handling-and-add-i18n-support
export default router;


export default router;
 main
