// /app/src/router/index.js

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

export default router;