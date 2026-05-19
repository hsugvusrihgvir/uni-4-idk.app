<template>
  <div class="empty-state">
    <div class="empty-icon">✦</div>
    <h3>{{ title }}</h3>
    <p>{{ text }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  text: { type: String, default: '' },
})
</script>
