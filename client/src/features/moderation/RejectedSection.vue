<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">rejected</p>
        <h2>Отклонённые идеи</h2>
      </div>
    </header>

    <div v-if="ideas.length" class="idea-grid">
      <article v-for="idea in ideas" :key="idea.id" class="idea-card" @click="$emit('open', idea)">
        <h3>{{ idea.title }}</h3>
        <p>{{ idea.description }}</p>
        <p class="reason-box">Причина: {{ idea.rejectionReason }}</p>

        <div class="card-actions">
          <button class="button primary" @click.stop="$emit('approve', idea.id)">одобрить</button>
          <button class="text-danger" @click.stop="$emit('remove', idea.id)">удалить</button>
        </div>
      </article>
    </div>

    <EmptyState
      v-else
      title="Отклонённых идей нет"
      text="Здесь будут идеи, которые модератор или админ не одобрили."
    />
  </section>
</template>

<script setup>
import EmptyState from '../../components/ui/EmptyState.vue'

defineProps({
  ideas: { type: Array, default: () => [] },
})

defineEmits(['open', 'approve', 'remove'])
</script>
