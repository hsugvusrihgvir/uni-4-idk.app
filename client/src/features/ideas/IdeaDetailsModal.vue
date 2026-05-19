<template>
  <AppModal :title="idea.title" label="карточка идеи" @close="$emit('close')">
    <div class="idea-details">
      <p>{{ idea.description }}</p>

      <div class="chip-row">
        <span class="chip">{{ statusLabel }}</span>
        <span class="chip" v-if="idea.isAnonymous">анонимно</span>
        <span class="chip" v-else>{{ idea.author }}</span>
        <span class="chip">{{ approvalPercent }}% одобрения</span>
      </div>

      <p v-if="idea.rejectionReason" class="reason-box">
        Причина: {{ idea.rejectionReason }}
      </p>
    </div>
  </AppModal>
</template>

<script setup>
import { computed } from 'vue'
import AppModal from '../../components/ui/AppModal.vue'

const props = defineProps({
  idea: { type: Object, required: true },
})

defineEmits(['close'])

const statusLabel = computed(() => {
  const labels = {
    approved: 'одобрено',
    pending: 'на модерации',
    rejected: 'отклонено',
  }

  return labels[props.idea.status] || props.idea.status
})

const approvalPercent = computed(() => {
  const total = props.idea.votesYes + props.idea.votesNo
  return total ? Math.round((props.idea.votesYes / total) * 100) : 0
})
</script>
