<script setup>
import { RouterView } from 'vue-router';
</script>

<template>
  <!-- 
    Этот компонент - точка входа для всех наших страниц.
    Он просто говорит: "Здесь будет отображаться текущая страница,
    определенная в роутере". Больше ему ничего не нужно.
  -->
  <RouterView />
</template>

<style scoped>
/* 
  Мы можем добавить сюда глобальные стили для лэйаута,
  например, отступы для всего приложения.
*/
#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  font-weight: normal;
}
</style>
