<template>
  <Modal :title="idea.title" :label="labels.card" @close="$emit('close')">
    <div class="idea-details">
      <p>{{ idea.description }}</p>

      <div class="chip-row">
        <span class="chip">{{ statusLabel }}</span>
        <span v-if="idea.isAnonymous" class="chip">{{ labels.anonymous }}</span>
        <span v-else class="chip">{{ idea.author }}</span>
        <span class="chip">{{ approvalPercent }}% {{ labels.approval }}</span>
      </div>

      <p v-if="idea.rejectionReason" class="reason-box">
        {{ labels.reason }}: {{ idea.rejectionReason }}
      </p>
    </div>
  </Modal>
</template>

<script setup>
import { computed } from 'vue'
import Modal from '../../components/ui/Modal.vue'

const props = defineProps({
  idea: { type: Object, required: true },
})

defineEmits(['close'])

const labels = {
  card: '\u043a\u0430\u0440\u0442\u043e\u0447\u043a\u0430 \u0438\u0434\u0435\u0438',
  anonymous: '\u0430\u043d\u043e\u043d\u0438\u043c\u043d\u043e',
  approval: '\u043e\u0434\u043e\u0431\u0440\u0435\u043d\u0438\u044f',
  reason: '\u041f\u0440\u0438\u0447\u0438\u043d\u0430',
}

const statusLabel = computed(() => {
  const labels = {
    approved: '\u043e\u0434\u043e\u0431\u0440\u0435\u043d\u043e',
    pending: '\u043d\u0430 \u043c\u043e\u0434\u0435\u0440\u0430\u0446\u0438\u0438',
    rejected: '\u043e\u0442\u043a\u043b\u043e\u043d\u0435\u043d\u043e',
  }

  return labels[props.idea.status] || props.idea.status
})

const approvalPercent = computed(() => {
  if (props.idea.approvalPercent !== undefined) return props.idea.approvalPercent

  const total = props.idea.votesYes + props.idea.votesNo
  return total ? Math.round((props.idea.votesYes / total) * 100) : 0
})
</script>
