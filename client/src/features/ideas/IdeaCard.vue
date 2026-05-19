<template>
  <article class="idea-card">
    <div class="idea-header">
      <h3>{{ idea.title }}</h3>
      <span class="idea-score">✦</span>
    </div>

    <div class="idea-main">
      <p>{{ idea.description }}</p>
    </div>

    <div class="idea-meta">
      <span>{{ idea.date }}</span>
      <span>{{ idea.isAnonymous ? 'анонимно' : idea.author }}</span>
    </div>

    <div class="idea-footer">
      <button class="text-danger">удалить</button>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  idea: { type: Object, required: true },
  canDelete: { type: Boolean, default: true },
})

defineEmits(['open', 'remove'])

const percent = computed(() => {
  const total = props.idea.votesYes + props.idea.votesNo
  return total ? Math.round((props.idea.votesYes / total) * 100) : 0
})
</script>
