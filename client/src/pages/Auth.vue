<template>
  <main class="auth-layout">
    <section class="mascot-panel cat-bg">
      <p></p>
    </section>

    <AuthBox @authenticated="$emit('authenticated')" />
  </main>
</template>

<script setup>
import AuthBox from '../features/auth/Auth.vue'

defineEmits(['authenticated'])
</script>
