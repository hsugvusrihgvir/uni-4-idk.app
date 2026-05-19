<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">одобренные</p>
        <h2>Все идеи</h2>
      </div>

      <input v-model="search" class="small-input" placeholder="поиск" />
    </header>

    <div v-if="filteredIdeas.length" class="idea-grid">
      <IdeaCard
        v-for="idea in filteredIdeas"
        :key="idea.id"
        :idea="idea"
        @open="$emit('open', $event)"
        @remove="$emit('remove', $event)"
      />
    </div>

    <EmptyState
      v-else
      title="Пока нет идей"
      text="Создайте новую идею или одобрите идею из модерации."
    />
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import IdeaCard from './IdeaCard.vue'
import EmptyState from '../../components/ui/EmptyState.vue'

const props = defineProps({
  ideas: { type: Array, default: () => [] },
})

defineEmits(['open', 'remove'])

const search = ref('')

const filteredIdeas = computed(() =>
  props.ideas.filter((idea) =>
    `${idea.title} ${idea.description}`.toLowerCase().includes(search.value.toLowerCase())
  )
)
</script>
