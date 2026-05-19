<template>
  <AppModal title="Отклонить идею" label="модерация" @close="$emit('close')">
    <form class="modal-form" @submit.prevent="submit">
      <p class="muted">{{ idea.title }}</p>

      <label class="field">
        Причина отклонения
        <textarea v-model="reason" placeholder="Причина отклонения"></textarea>
      </label>

      <button class="button primary">Не одобрить</button>
    </form>
  </AppModal>
</template>

<script setup>
import { ref } from 'vue'
import AppModal from '../../components/ui/AppModal.vue'

const props = defineProps({
  idea: { type: Object, required: true },
})

const emit = defineEmits(['close', 'confirm'])
const reason = ref('')

function submit() {
  emit('confirm', props.idea.id, reason.value)
}
</script>
