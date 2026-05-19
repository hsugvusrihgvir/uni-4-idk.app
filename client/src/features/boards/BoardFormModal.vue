<template>
  <AppModal title="Создать доску" label="новая доска" @close="$emit('close')">
    <form class="modal-form" @submit.prevent="submit">
      <label class="field">
        Название
        <input v-model="form.title" placeholder="Доска 1" required />
      </label>

      <label class="field">
        Описание
        <textarea v-model="form.description" placeholder="Описание доски"></textarea>
      </label>

      <button class="button primary">Создать</button>
    </form>
  </AppModal>
</template>

<script setup>
import { reactive } from 'vue'
import AppModal from '../../components/ui/AppModal.vue'

const emit = defineEmits(['close', 'save'])

const form = reactive({
  title: '',
  description: '',
})

function submit() {
  emit('save', { ...form })
}
</script>
