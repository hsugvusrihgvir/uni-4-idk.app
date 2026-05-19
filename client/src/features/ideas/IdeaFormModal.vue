<template>
  <AppModal title="Предложить идею" label="новая идея" @close="$emit('close')">
    <form class="modal-form" @submit.prevent="submit">
      <label class="field">
        Название
        <input v-model="form.title" placeholder="Идея 1" required />
      </label>

      <label class="field">
        Описание
        <textarea v-model="form.description" placeholder="Описание идеи" required></textarea>
      </label>

      <label v-if="allowAnonymous" class="checkbox-field">
        <input v-model="form.isAnonymous" type="checkbox" />
        отправить анонимно
      </label>

      <button class="button primary">Отправить</button>
    </form>
  </AppModal>
</template>

<script setup>
import { reactive } from 'vue'
import AppModal from '../../components/ui/AppModal.vue'

defineProps({
  allowAnonymous: { type: Boolean, default: true },
})

const emit = defineEmits(['close', 'save'])

const form = reactive({
  title: '',
  description: '',
  isAnonymous: true,
})

function submit() {
  emit('save', { ...form })
}
</script>
