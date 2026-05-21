<template>
  <Modal title="Создать доску" label="новая доска" @close="$emit('close')">
    <form class="modal-form" novalidate @submit.prevent="submit">
      <p v-if="error" class="form-message error">{{ error }}</p>

      <label class="field">
        Название
        <input v-model.trim="form.title" placeholder="Доска 1" />
      </label>

      <label class="field">
        Описание
        <textarea v-model.trim="form.description" placeholder="Описание доски"></textarea>
      </label>

      <button class="button primary">Создать</button>
    </form>
  </Modal>
</template>

<script setup>
import { reactive, ref } from 'vue'
import Modal from '../../components/ui/Modal.vue'

const emit = defineEmits(['close', 'save'])
const error = ref('')
const form = reactive({ title: '', description: '' })

function submit() {
  if (!form.title) {
    error.value = 'Введите название доски.'
    return
  }

  error.value = ''
  emit('save', { ...form })
}
</script>
