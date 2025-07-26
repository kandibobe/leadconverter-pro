// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import QuizView from '../views/QuizView.vue'
import AdminLayout from '../layouts/AdminLayout.vue' // <-- Импортируем новый лэйаут
import DashboardView from '../views/admin/DashboardView.vue' // <-- Импортируем страницы админки
import LeadsView from '../views/admin/LeadsView.vue'

// Простая проверка "авторизации" для MVP
const requireAuth = (to, from, next) => {
  // В будущем здесь будет проверка настоящего токена
  if (localStorage.getItem('admin-token')) {
    next()
  } else {
    // Для простоты, если токена нет, можно редиректить на главную
    // или показать страницу логина (которой пока нет)
    console.warn('Access denied. No admin-token found in localStorage.')
    alert('Доступ запрещен. Установите "admin-token" в localStorage для доступа.')
    next('/')
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/quiz/:id',
      name: 'quiz',
      component: QuizView,
      props: true
    },
    // Группа роутов для админ-панели
    {
      path: '/admin',
      component: AdminLayout,
      beforeEnter: requireAuth, // <-- Защищаем все дочерние роуты
      children: [
        {
          path: 'dashboard',
          name: 'admin-dashboard',
          component: DashboardView
        },
        {
          path: 'leads',
          name: 'admin-leads',
          component: LeadsView
        },
        // Редирект, чтобы при входе на /admin сразу открывался дашборд
        {
          path: '',
          redirect: '/admin/dashboard'
        }
      ]
    }
  ]
})

 codex/add-newline-at-eof-for-project-files
export default router;

export default router
 main
