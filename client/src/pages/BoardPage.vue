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
          :class="{ active: activeSection === item.id }"
          @click="activeSection = item.id"
        >
          {{ item.title }}
        </button>
      </nav>
    </aside>

    <section class="workspace-content">
      <header class="topbar">
        <div>
          <p class="eyebrow">{{ board.title }}</p>
          <h1>{{ currentSectionTitle }}</h1>
        </div>

        <div class="topbar-actions">
          <button
            v-if="activeSection === 'ideas'"
            class="button primary"
            @click="showIdeaModal = true"
          >
            предложить идею
          </button>
          <button class="button ghost" @click="showExportModal = true">экспорт txt</button>
          <button class="button ghost" @click="showAiModal = true">ии-сводка</button>
        </div>
      </header>

      <IdeasSection
        v-if="activeSection === 'ideas'"
        :ideas="approvedIdeas"
        @open="selectedIdea = $event"
        @remove="deleteIdea"
      />

      <VotingSection
        v-else-if="activeSection === 'voting'"
        :ideas="approvedIdeas"
        :results="voteResults"
        @open="selectedIdea = $event"
        @vote="voteIdea"
      />

      <ModerationSection
        v-else-if="activeSection === 'moderation'"
        :ideas="pendingIdeas"
        @open="selectedIdea = $event"
        @approve="approveIdea"
        @reject="rejectTarget = $event"
      />

      <RejectedSection
        v-else-if="activeSection === 'rejected'"
        :ideas="rejectedIdeas"
        @open="selectedIdea = $event"
        @approve="approveIdea"
        @remove="deleteIdea"
      />

      <MembersSection
        v-else-if="activeSection === 'members'"
        :board-id="board.id"
        :members="board.members"
        @add="addMember(board.id, $event)"
        @remove="removeMember(board.id, $event)"
        @role="toggleModerator(board.id, $event)"
      />

      <SettingsSection
        v-else
        :board="board"
        @save="updateBoard(board.id, $event)"
        @transfer-admin="transferAdmin(board.id, $event)"
      />
    </section>

    <IdeaFormModal
      v-if="showIdeaModal"
      :allow-anonymous="board.allowAnonymous"
      @close="showIdeaModal = false"
      @save="handleCreateIdea"
    />

    <IdeaDetailsModal
      v-if="selectedIdea"
      :idea="selectedIdea"
      @close="selectedIdea = null"
    />

    <RejectIdeaModal
      v-if="rejectTarget"
      :idea="rejectTarget"
      @close="rejectTarget = null"
      @confirm="handleReject"
    />

    <ExportIdeasModal
      v-if="showExportModal"
      :ideas="voteResults"
      @close="showExportModal = false"
    />

    <AiSummaryModal
      v-if="showAiModal"
      :ideas="voteResults"
      :board="board"
      @close="showAiModal = false"
    />
  </main>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import IdeasSection from '../features/ideas/IdeasSection.vue'
import IdeaFormModal from '../features/ideas/IdeaFormModal.vue'
import IdeaDetailsModal from '../features/ideas/IdeaDetailsModal.vue'
import VotingSection from '../features/voting/VotingSection.vue'
import ModerationSection from '../features/moderation/ModerationSection.vue'
import RejectedSection from '../features/moderation/RejectedSection.vue'
import RejectIdeaModal from '../features/moderation/RejectIdeaModal.vue'
import MembersSection from '../features/members/MembersSection.vue'
import SettingsSection from '../features/settings/SettingsSection.vue'
import ExportIdeasModal from '../features/export/ExportIdeasModal.vue'
import AiSummaryModal from '../features/ai/AiSummaryModal.vue'
import { useAppStore } from '../store/useAppStore'

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
} = useAppStore()

const activeSection = ref('ideas')
const showIdeaModal = ref(false)
const showExportModal = ref(false)
const showAiModal = ref(false)
const selectedIdea = ref(null)
const rejectTarget = ref(null)

const sections = [
  { id: 'ideas', title: 'Идеи' },
  { id: 'voting', title: 'Голосование' },
  { id: 'moderation', title: 'Модерация' },
  { id: 'rejected', title: 'Отклонённые' },
  { id: 'members', title: 'Участники' },
  { id: 'settings', title: 'Настройки' },
]

const board = computed(() => getBoard(props.boardId) || { members: [] })
const allIdeas = computed(() => getBoardIdeas(props.boardId))
const approvedIdeas = computed(() => allIdeas.value.filter((idea) => idea.status === 'approved'))
const pendingIdeas = computed(() => allIdeas.value.filter((idea) => idea.status === 'pending'))
const rejectedIdeas = computed(() => allIdeas.value.filter((idea) => idea.status === 'rejected'))
const voteResults = computed(() => getVoteResults(props.boardId))

const currentSectionTitle = computed(() =>
  sections.find((section) => section.id === activeSection.value)?.title || 'Доска'
)

onMounted(loadData)
watch(() => props.boardId, loadData)

async function loadData() {
  await loadBoard(props.boardId)
  await loadIdeas(props.boardId)
}

async function handleCreateIdea(payload) {
  await createIdea(props.boardId, payload)
  showIdeaModal.value = false
}

function handleReject(ideaId, reason) {
  rejectIdea(ideaId, reason)
  rejectTarget.value = null
}
</script>
