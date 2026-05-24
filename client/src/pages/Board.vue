<template>
  <main class="workspace">
    <aside class="sidebar">
      <button class="back-button" @click="$emit('back')">← доски</button>

      <section class="sidebar-card">
        <p class="eyebrow">доска</p>
        <h2>{{ board.title }}</h2>
        <p>{{ board.description }}</p>
      </section>

      <nav class="sidebar-nav">
        <button
          v-for="item in sections"
          :key="item.id"
          :class="{ active: tab === item.id }"
          @click="tab = item.id"
        >
          {{ item.title }}
        </button>
      </nav>
    </aside>

    <section class="workspace-content">
      <header class="topbar">
        <div>
          <p class="eyebrow">{{ board.title }}</p>
          <h1>{{ tabTitle }}</h1>
        </div>

        <div class="topbar-actions">
          <button v-if="tab === 'ideas'" class="button primary" @click="ideaOpen = true">
            предложить идею
          </button>
          <button class="button ghost" @click="exportOpen = true">экспорт отчета</button>
          <button class="button ghost" @click="aiOpen = true">сводка</button>
        </div>
      </header>

      <Ideas
        v-if="tab === 'ideas'"
        :ideas="okIdeas"
        @open="chosenIdea = $event"
        @remove="deleteIdea"
      />

      <Voting
        v-else-if="tab === 'voting'"
        :ideas="okIdeas"
        :results="results"
        :voting="activeVoting(board.id)"
        @open="chosenIdea = $event"
        @vote="voteIdea"
        @create="createVoting(board.id, $event)"
        @delete="deleteVoting(board.id, $event)"
      />

      <Moderation
        v-else-if="tab === 'moderation'"
        :ideas="waitIdeas"
        @open="chosenIdea = $event"
        @approve="approveIdea"
        @reject="badIdea = $event"
      />

      <Rejected
        v-else-if="tab === 'rejected'"
        :ideas="badIdeas"
        @open="chosenIdea = $event"
        @approve="approveIdea"
        @remove="deleteIdea"
      />

      <Members
        v-else-if="tab === 'members'"
        :board-id="board.id"
        :members="board.members"
        @add="addMember(board.id, $event)"
        @remove="removeMember(board.id, $event)"
        @role="toggleModerator(board.id, $event)"
      />

      <Settings
        v-else
        :board="board"
        @save="updateBoard(board.id, $event)"
        @transfer-admin="transferAdmin(board.id, $event)"
      />
    </section>

    <IdeaForm
      v-if="ideaOpen"
      :allow-anonymous="board.allowAnonymous"
      @close="ideaOpen = false"
      @save="saveIdea"
    />

    <IdeaInfo v-if="chosenIdea" :idea="chosenIdea" @close="chosenIdea = null" />

    <RejectModal
      v-if="badIdea"
      :idea="badIdea"
      @close="badIdea = null"
      @confirm="saveReject"
    />

    <ExportModal v-if="exportOpen" :ideas="results" :board="board" @close="exportOpen = false" />
    <AiModal v-if="aiOpen" :ideas="results" :board="board" @close="aiOpen = false" />
  </main>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import Ideas from '../features/ideas/Ideas.vue'
import IdeaForm from '../features/ideas/IdeaForm.vue'
import IdeaInfo from '../features/ideas/IdeaInfo.vue'
import Voting from '../features/voting/Voting.vue'
import Moderation from '../features/moderation/Moderation.vue'
import Rejected from '../features/moderation/Rejected.vue'
import RejectModal from '../features/moderation/RejectModal.vue'
import Members from '../features/members/Members.vue'
import Settings from '../features/settings/Settings.vue'
import ExportModal from '../features/export/ExportModal.vue'
import AiModal from '../features/ai/AiModal.vue'
import { useStore } from '../store/store'

const props = defineProps({
  boardId: { type: String, required: true },
})

defineEmits(['back'])

const {
  getBoard,
  getBoardIdeas,
  getVoteResults,
  loadBoard,
  loadIdeas,
  loadModerationIdeas,
  createIdea,
  deleteIdea,
  approveIdea,
  rejectIdea,
  voteIdea,
  addMember,
  removeMember,
  toggleModerator,
  updateBoard,
  transferAdmin,
  activeVoting,
  loadVotings,
  createVoting,
  deleteVoting,
  connectIdeasWs,
} = useStore()

const tab = ref('ideas')
const ideaOpen = ref(false)
const exportOpen = ref(false)
const aiOpen = ref(false)
const chosenIdea = ref(null)
const badIdea = ref(null)

const sections = [
  { id: 'ideas', title: 'Идеи' },
  { id: 'voting', title: 'Голосование' },
  { id: 'moderation', title: 'Модерация' },
  { id: 'rejected', title: 'Отклоненные' },
  { id: 'members', title: 'Участники' },
  { id: 'settings', title: 'Настройки' },
]

const board = computed(() => getBoard(props.boardId) || { members: [] })
const ideas = computed(() => getBoardIdeas(props.boardId))
const okIdeas = computed(() => ideas.value.filter((idea) => idea.status === 'approved'))
const waitIdeas = computed(() => ideas.value.filter((idea) => idea.status === 'pending'))
const badIdeas = computed(() => ideas.value.filter((idea) => idea.status === 'rejected'))
const results = computed(() => getVoteResults(props.boardId))
const tabTitle = computed(() => sections.find((section) => section.id === tab.value)?.title || 'Доска')

onMounted(loadData)
watch(() => props.boardId, loadData)

async function loadData() {
  await loadBoard(props.boardId)
  await loadIdeas(props.boardId)
  await loadModerationIdeas(props.boardId).catch(() => [])
  await loadVotings(props.boardId).catch(() => [])
  connectIdeasWs(props.boardId)
}

async function saveIdea(form) {
  await createIdea(props.boardId, form)
  ideaOpen.value = false
}

async function saveReject(ideaId, reason) {
  await rejectIdea(ideaId, reason)
  badIdea.value = null
}
</script>
