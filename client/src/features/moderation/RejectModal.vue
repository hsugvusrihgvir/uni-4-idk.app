<template>
  <Modal title="Отклонить идею" label="модерация" @close="$emit('close')">
    <form class="modal-form" @submit.prevent="submit">
      <p class="muted">{{ idea.title }}</p>

      <label class="field">
        Причина отклонения
        <textarea v-model="reason" placeholder="Причина отклонения"></textarea>
      </label>

      <button class="button primary">не одобрять</button>
    </form>
  </Modal>
</template>

<script setup>
import { ref } from 'vue'
import Modal from '../../components/ui/Modal.vue'

const props = defineProps({
  idea: { type: Object, required: true },
})

const emit = defineEmits(['close', 'confirm'])
const reason = ref('')

function submit() {
  emit('confirm', props.idea.id, reason.value)
}
</script>