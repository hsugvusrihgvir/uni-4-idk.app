<template>
  <main class="auth-layout">
    <section class="mascot-panel cat-bg">
      <p></p>
    </section>

    <AuthForm @submit="$emit('login', $event)" />
  </main>
</template>

<script setup>
import AuthForm from '../features/auth/AuthForm.vue'

defineEmits(['login'])
</script>
