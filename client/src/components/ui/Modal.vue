<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <section class="modal-card" :class="{ wide }">
      <header class="modal-header">
        <div>
          <p v-if="label" class="eyebrow">{{ label }}</p>
          <h2>{{ title }}</h2>
        </div>
        <button class="round-button" type="button" @click="$emit('close')">×</button>
      </header>

      <slot />
    </section>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  label: { type: String, default: '' },
  wide: { type: Boolean, default: false },
})

defineEmits(['close'])
</script>
