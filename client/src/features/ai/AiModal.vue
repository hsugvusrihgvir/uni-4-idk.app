<template>
  <Modal title="ИИ-сводка" label="в разработке" wide @close="$emit('close')">
    <section class="empty-state">
      <p class="eyebrow">скоро</p>
      <h2>Функция в разработке</h2>
      <p>
        Здесь появится ИИ-сводка по идеям доски: краткие выводы, общие темы и
        предложения по следующим шагам.
      </p>
      <button class="button primary" type="button" @click="$emit('close')">понятно</button>
    </section>
  </Modal>
</template>

<script setup>
import Modal from '../../components/ui/Modal.vue'

defineProps({
  ideas: { type: Array, default: () => [] },
  board: { type: Object, required: true },
})

defineEmits(['close'])
</script>
