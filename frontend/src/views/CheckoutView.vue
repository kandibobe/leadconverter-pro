<script setup>
import { ref } from 'vue';

const email = ref('');
function submit() {
  alert(`Processing payment for ${email.value}`);
}
</script>

<template>
  <div class="checkout">
    <h1>Choose Plan</h1>
    <form @submit.prevent="submit">
      <input v-model="email" type="email" placeholder="Email" required />
      <button type="submit">Pay</button>
    </form>
  </div>
</template>

<style scoped>
.checkout {
  max-width: 400px;
  margin: 2rem auto;
}
</style>
