import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    // ДОБАВЛЯЕМ НОВЫЙ МАРШРУТ
    // :id - это динамический параметр, который будет доступен в компоненте
    {
      path: '/quiz/:id',
      name: 'quiz',
      // Ленивая загрузка (lazy-loading): компонент будет загружен только тогда,
      // когда пользователь перейдет на этот маршрут. Это улучшает производительность.
      component: () => import('../views/QuizView.vue')
    }
  ]
});

export default router;