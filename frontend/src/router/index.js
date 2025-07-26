 HEAD
// /app/src/router/index.js

// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import QuizView from '../views/QuizView.vue'
import AdminLayout from '../layouts/AdminLayout.vue' // <-- Импортируем новый лэйаут
import DashboardView from '../views/DashboardView.vue' // <-- Импортируем страницы админки
import LeadsView from '../views/admin/LeadsView.vue'
 ff32d054763a076e239d8b550239cda8bc239e4e

import { createRouter, createWebHistory } from 'vue-router';

// Импорты стали чистыми и понятными
import QuizView from '@/views/QuizView.vue';
import AdminLayout from '@/layouts/AdminLayout.vue';
import DashboardView from '@/views/admin/DashboardView.vue';

const routes = [
  {
    path: '/',
    name: 'Quiz',
    component: QuizView
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: DashboardView
      },
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

 HEAD
export default router;

 ff32d054763a076e239d8b550239cda8bc239e4e
