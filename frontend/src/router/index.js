import { createRouter, createWebHistory } from 'vue-router';

import QuizView from '@/views/QuizView.vue';
import AdminLayout from '@/layouts/AdminLayout.vue';
import DashboardView from '@/views/admin/DashboardView.vue';
import LeadsView from '@/views/admin/LeadsView.vue';

const routes = [
  {
    path: '/',
    name: 'Quiz',
    component: QuizView,
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: '', name: 'Dashboard', component: DashboardView },
      { path: 'leads', name: 'Leads', component: LeadsView },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

