<template>
  <Modal :title="title" :label="label" @close="$emit('cancel')">
    <div class="modal-form">
      <p class="confirm-text">{{ text }}</p>

      <div class="modal-actions">
        <button class="button ghost" type="button" @click="$emit('cancel')">отмена</button>
        <button class="button danger" type="button" @click="$emit('confirm')">{{ confirmText }}</button>
      </div>
    </div>
  </Modal>
</template>

<script setup>
import Modal from './Modal.vue'

defineProps({
  title: { type: String, required: true },
  text: { type: String, required: true },
  label: { type: String, default: 'подтверждение' },
  confirmText: { type: String, default: 'удалить' },
})

defineEmits(['confirm', 'cancel'])
</script>
