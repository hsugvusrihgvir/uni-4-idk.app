<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">активное голосование</p>
        <h2>{{ voting ? names[voting.type] : 'Голосование не создано' }}</h2>
      </div>

      <div class="topbar-actions">
        <button v-if="!voting" class="button primary" @click="$emit('create', 'yes_no')">
          создать
        </button>
        <button v-if="!voting" class="button ghost" @click="$emit('create', 'like')">
          like
        </button>
        <button v-if="voting" class="button ghost" @click="$emit('delete', voting.id)">
          удалить
        </button>
      </div>
    </header>

    <div v-if="voting && ideas.length" class="vote-list">
      <article v-for="idea in ideas" :key="idea.id" class="vote-card">
        <div class="vote-text">
          <h3>{{ idea.title }}</h3>
          <p>{{ idea.description }}</p>
        </div>

        <div class="vote-actions">
          <button class="button ghost" @click="$emit('open', idea)">открыть</button>
          <button class="button primary" @click="$emit('vote', idea.id)">голос</button>
        </div>
      </article>
    </div>

    <Empty
      v-else
      title="Нет идей для голосования"
      text="В голосовании участвуют только одобренные идеи."
    />

    <section class="results-panel">
      <h3>Результаты</h3>

      <button v-for="result in results" :key="result.id" class="result-row" @click="$emit('open', result)">
        <span>{{ result.title }}</span>
        <strong>{{ result.votesCount }} / {{ result.approvalPercent }}%</strong>
      </button>
    </section>
  </section>
</template>

<script setup>
import Empty from '../../components/ui/Empty.vue'

defineProps({
  ideas: { type: Array, default: () => [] },
  results: { type: Array, default: () => [] },
  voting: { type: Object, default: null },
})

defineEmits(['open', 'vote', 'create', 'delete'])

const names = {
  like: 'Like-голосование',
  yes_no: 'Голосование',
}
</script>
