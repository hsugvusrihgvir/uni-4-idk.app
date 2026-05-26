<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">активное голосование</p>
        <h2>{{ voting ? modes[voting.type].title : 'Голосование не создано' }}</h2>
        <p v-if="voting">{{ modes[voting.type].hint }}</p>
      </div>

      <div v-if="canManage" class="topbar-actions">
        <button v-if="!voting" class="button primary" @click="$emit('create')">
          создать голосование
        </button>
        <button v-if="voting" class="button ghost" @click="$emit('delete', voting.id)">
          удалить
        </button>
      </div>
    </header>

    <div v-if="voting" class="voting-layout">
      <section class="voting-block">
        <div class="block-title">
          <span class="block-icon">1</span>
          <h3>Идеи для выбора</h3>
        </div>

        <div v-if="ideas.length" class="vote-list">
          <article v-for="idea in ideas" :key="idea.id" class="vote-card">
            <div class="vote-text">
              <h3>{{ idea.title }}</h3>
              <p>{{ idea.description }}</p>
            </div>

            <div class="vote-actions">
              <button class="button ghost" @click="$emit('open', idea)">открыть</button>
              <button
                class="button"
                :class="isVoted(idea.id) ? 'ghost' : 'primary'"
                @click="$emit('vote', idea.id)"
              >
                {{ isVoted(idea.id) ? 'отменить' : 'голос' }}
              </button>
            </div>
          </article>
        </div>

        <Empty
          v-else
          title="Нет идей для голосования"
          text="В голосовании участвуют только одобренные идеи."
        />
      </section>

      <section class="results-panel">
        <div class="results-head">
          <div class="block-title">
            <span class="block-icon">%</span>
            <h3>Результаты</h3>
          </div>
          <span class="chip">{{ totalVotes }} голосов</span>
        </div>

        <div v-if="results.length" class="results-list">
          <button
            v-for="result in results"
            :key="result.id"
            class="result-row"
            :class="{ voted: result.userVoted }"
            @click="$emit('open', result)"
          >
            <span>{{ result.title }}</span>
            <strong>{{ result.votesCount }} / {{ result.approvalPercent }}%</strong>
            <span class="result-bar" :style="{ width: `${result.approvalPercent}%` }"></span>
          </button>
        </div>

        <Empty
          v-else
          title="Результатов пока нет"
          text="Они появятся после первого голоса."
        />
      </section>
    </div>

    <Empty
      v-else
      title="Голосование не создано"
      text="Администратор может создать голосование и выбрать его тип."
    />
  </section>
</template>

<script setup>
import { computed } from 'vue'
import Empty from '../../components/ui/Empty.vue'

const props = defineProps({
  ideas: { type: Array, default: () => [] },
  results: { type: Array, default: () => [] },
  voting: { type: Object, default: null },
  canManage: { type: Boolean, default: false },
})

defineEmits(['open', 'vote', 'create', 'delete'])

const modes = {
  like: {
    title: 'Несколько идей',
    hint: 'Можно выбрать сколько угодно идей и отменить любой голос.',
  },
  yes_no: {
    title: 'Один выбор',
    hint: 'Можно выбрать только одну идею. Новый голос заменит старый.',
  },
}

const votedIds = computed(() => new Set(props.results.filter((item) => item.userVoted).map((item) => item.id)))
const totalVotes = computed(() => props.results.reduce((sum, item) => sum + item.votesCount, 0))

function isVoted(ideaId) {
  return votedIds.value.has(ideaId)
}
</script>
