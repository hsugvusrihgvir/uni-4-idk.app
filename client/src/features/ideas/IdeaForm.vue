<template>
  <Modal title="Предложить идею" label="новая идея" @close="$emit('close')">
    <form class="modal-form" novalidate @submit.prevent="submit">
      <p v-if="error" class="form-message error">{{ error }}</p>

      <label class="field">
        Название
        <input v-model.trim="form.title" placeholder="Идея 1" />
      </label>

      <label class="field">
        Описание
        <textarea v-model.trim="form.description" placeholder="Описание идеи"></textarea>
      </label>

      <label v-if="allowAnonymous" class="checkbox-field">
        <input v-model="form.isAnonymous" type="checkbox" />
        отправить анонимно
      </label>

      <button class="button primary">Отправить</button>
    </form>
  </Modal>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import Modal from '../../components/ui/Modal.vue'

const props = defineProps({
  allowAnonymous: { type: Boolean, default: true },
})

const emit = defineEmits(['close', 'save'])
const error = ref('')
const form = reactive({ title: '', description: '', isAnonymous: false })

watch(
  () => props.allowAnonymous,
  (allowAnonymous) => {
    if (!allowAnonymous) form.isAnonymous = false
  },
  { immediate: true }
)

function submit() {
  if (!form.title) {
    error.value = 'Введите название идеи.'
    return
  }

  if (!form.description) {
    error.value = 'Введите описание идеи.'
    return
  }

  error.value = ''
  emit('save', { ...form, isAnonymous: props.allowAnonymous ? form.isAnonymous : false })
}
</script>
