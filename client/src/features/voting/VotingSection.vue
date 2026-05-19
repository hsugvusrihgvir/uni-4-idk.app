<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">активное голосование</p>
        <h2>Да / нет по каждой идее</h2>
      </div>
      <button class="button ghost">⋯</button>
    </header>

    <div v-if="ideas.length" class="vote-list">
      <article v-for="idea in ideas" :key="idea.id" class="vote-card">
        <div class="vote-text">
          <h3>{{ idea.title }}</h3>
          <p>{{ idea.description }}</p>
        </div>

        <div class="vote-actions">
          <button class="button ghost" @click="$emit('open', idea)">открыть</button>
          <button class="button primary" @click="$emit('vote', idea.id, 'yes')">да</button>
          <button class="button ghost" @click="$emit('vote', idea.id, 'no')">нет</button>
        </div>
      </article>
    </div>

    <EmptyState
      v-else
      title="Нет идей для голосования"
      text="В голосовании участвуют только одобренные идеи."
    />

    <section class="results-panel">
      <h3>Результаты</h3>

      <button
        v-for="result in results"
        :key="result.id"
        class="result-row"
        @click="$emit('open', result)"
      >
        <span>{{ result.title }}</span>
        <strong>{{ result.approvalPercent }}%</strong>
      </button>
    </section>
  </section>
</template>

<script setup>
import EmptyState from '../../components/ui/EmptyState.vue'

defineProps({
  ideas: { type: Array, default: () => [] },
  results: { type: Array, default: () => [] },
})

defineEmits(['open', 'vote'])
</script>
