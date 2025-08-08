import { createRouter, createWebHistory } from 'vue-router';
import remoteRoutes from './remoteRoutes';
import HomePage from './HomePage.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomePage },
    ...remoteRoutes,
    { path: '/:pathMatch(.*)*', component: () => import('./NotFound.vue') },
  ],
});

export default router;

