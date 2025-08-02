<script setup>
// ... (логика для v-model и вызова authStore.login)
</script>
<template>
  <div class="login-container">
    <h2>Вход в панель управления</h2>
    <form @submit.prevent="handleLogin">
      <input type="email" v-model="email" placeholder="Email" required />
      <input type="password" v-model="password" placeholder="Пароль" required />
      <p v-if="authStore.error" class="error-text">{{ authStore.error }}</p>
      <button type="submit">Войти</button>
    </form>
  </div>
</template>
<style scoped> /* ... стили для формы ... */ </style>