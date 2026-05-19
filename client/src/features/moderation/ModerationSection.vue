<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">pending</p>
        <h2>Модерация</h2>
      </div>
    </header>

    <div v-if="ideas.length" class="row-list">
      <article v-for="idea in ideas" :key="idea.id" class="list-card">
        <button class="list-main" @click="$emit('open', idea)">
          <h3>{{ idea.title }}</h3>
          <p>{{ idea.description }}</p>
        </button>

        <div class="list-actions">
          <button class="button primary" @click="$emit('approve', idea.id)">одобрить</button>
          <button class="button ghost" @click="$emit('reject', idea)">не одобрить</button>
        </div>
      </article>
    </div>

    <EmptyState
      v-else
      title="Очередь пустая"
      text="Новые идеи появятся здесь, если выключено автоодобрение."
    />
  </section>
</template>

<script setup>
import EmptyState from '../../components/ui/EmptyState.vue'

defineProps({
  ideas: { type: Array, default: () => [] },
})

defineEmits(['open', 'approve', 'reject'])
</script>
