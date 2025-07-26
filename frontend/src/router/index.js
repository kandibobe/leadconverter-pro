import { createRouter, createWebHistory } from 'vue-router';

// --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
// Старые пути были правильными, просто копируем их логику.
// Все "View" компоненты лежат в папке /src/views/

import QuizView from '../views/QuizView.vue';
import AdminLayout from '../layouts/AdminLayout.vue'; // Лэйаут для админки

// Вот проблемная строка. Заменяем './' на '../'
// БЫЛО: import DashboardView from './views/admin/DashboardView.vue'
import DashboardView from '../views/admin/DashboardView.vue'; // <-- ПРАВИЛЬНЫЙ ПУТЬ

// Предположим, у вас есть и другие страницы в админке, добавим их для примера
// import SettingsView from '../views/admin/SettingsView.vue';
// import LeadsView from '../views/admin/LeadsView.vue';


const routes = [
  // Маршрут для клиентского квиза
  {
    path: '/',
    name: 'Quiz',
    component: QuizView
  },

  // Маршруты для административной панели
  {
    path: '/admin',
    component: AdminLayout, // Используем специальный лэйаут для всех дочерних админ-страниц
    children: [
      {
        path: '', // Пустой путь для /admin -> редирект на дашборд или сам дашборд
        name: 'Dashboard',
        component: DashboardView
      },
      // Пример других маршрутов в админке
      // {
      //   path: 'leads',
      //   name: 'AdminLeads',
      //   component: LeadsView
      // },
      // {
      //   path: 'settings',
      //   name: 'AdminSettings',
      //   component: SettingsView
      // }
    ]
  },
  
  // Можно добавить обработку страницы 404
  // { 
  //   path: '/:pathMatch(.*)*', 
  //   name: 'NotFound', 
  //   component: () => import('../views/NotFoundView.vue')
  // }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;