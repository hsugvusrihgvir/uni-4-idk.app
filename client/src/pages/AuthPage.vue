<template>
  <main class="auth-layout">
    <section class="mascot-panel cat-bg">
      <p></p>
    </section>

    <AuthForm @authenticated="$emit('authenticated')" />
  </main>
</template>

<script setup>
import AuthForm from '../features/auth/AuthForm.vue'

defineEmits(['authenticated'])
</script>
