<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <main class="home-view-container">
    <h1>Welcome to LeadConverter Pro</h1>
    <p class="subtitle">
      Готовы рассчитать стоимость вашего проекта?
    </p>
    <div class="cta-container">
      <!-- RouterLink - это компонент Vue Router для создания навигационных ссылок -->
      <RouterLink to="/quiz/1" class="cta-button">
        Начать расчет
      </RouterLink>
    </div>
  </main>
</template>

<style scoped>
.home-view-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
  text-align: center;
}
.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-top: 0.5rem;
}
.cta-container {
  margin-top: 2.5rem;
}
.cta-button {
  display: inline-block;
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  font-weight: bold;
  color: #fff;
  background-color: #42b983; /* Зеленый цвет Vue */
  border-radius: 8px;
  text-decoration: none;
  transition: background-color 0.3s ease;
}
.cta-button:hover {
  background-color: #33a06f;
}
</style>