<!-- frontend/src/layouts/AdminLayout.vue -->
<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <h2 class="sidebar-title">LeadConverter</h2>
      <nav>
        <router-link
          to="/admin"
          class="nav-link"
          active-class=""
          exact-active-class="router-link-active"
        >
          Дашборд
        </router-link>
        <router-link to="/admin/leads" class="nav-link">Лиды</router-link>
      </nav>
      <button @click="logout" class="logout-button">Выйти</button>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const logout = () => {
  localStorage.removeItem('admin-token');
  router.push('/');
};
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 250px;
  background-color: #2c3e50;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
}
.sidebar-title {
  text-align: center;
  margin-bottom: 30px;
}
.nav-link {
  display: block;
  color: #bdc3c7;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 4px;
  margin-bottom: 10px;
  transition: background-color 0.3s, color 0.3s;
}
.nav-link:hover, .router-link-active {
  background-color: #34495e;
  color: white;
}
.main-content {
  flex-grow: 1;
  padding: 30px;
  background-color: #f4f6f9;
}
.logout-button {
  margin-top: auto;
  padding: 10px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.logout-button:hover {
  background-color: #c0392b;
}
</style>