<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">модерация</p>
        <h2>Очередь идей</h2>
      </div>
    </header>

    <div v-if="ideas.length" class="row-list">
      <article v-for="idea in ideas" :key="idea.id" class="list-card">
        <button class="list-main" @click="$emit('open', idea)">
          <h3>{{ idea.title }}</h3>
          <p>{{ idea.description }}</p>
        </button>

        <div class="list-actions">
          <button class="button primary" :disabled="busyIds.includes(idea.id)" @click="$emit('approve', idea.id)">
            одобрить
          </button>
          <button class="button ghost" :disabled="busyIds.includes(idea.id)" @click="$emit('reject', idea)">
            отклонить
          </button>
        </div>
      </article>
    </div>

    <Empty
      v-else
      title="Очередь пустая"
      text="Новые идеи появятся здесь, если включена модерация."
    />
  </section>
</template>

<script setup>
import Empty from '../../components/ui/Empty.vue'

defineProps({
  ideas: { type: Array, default: () => [] },
  busyIds: { type: Array, default: () => [] },
})

defineEmits(['open', 'approve', 'reject'])
</script>
