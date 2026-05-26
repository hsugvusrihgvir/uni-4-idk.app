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
          <button v-if="canModerate" class="button ghost" @click="exportOpen = true">экспорт отчета</button>
          <button v-if="canModerate" class="button ghost" @click="aiOpen = true">сводка</button>
        </div>
      </header>

      <Ideas
        v-if="tab === 'ideas'"
        :ideas="approvedIdeas"
        :can-delete="canModerate"
        :current-username="currentUsername"
        @open="idea = $event"
        @remove="askDeleteIdea"
        @open-author="openIdeaAuthor"
      />

      <Voting
        v-else-if="tab === 'voting'"
        :ideas="approvedIdeas"
        :results="voteResults"
        :voting="activeVoting(board.id)"
        :can-manage="isAdmin"
        @open="idea = $event"
        @vote="voteIdea"
        @create="votingCreateOpen = true"
        @delete="askDeleteVoting"
      />

      <Moderation
        v-else-if="tab === 'moderation' && canModerate"
        :ideas="pendingIdeas"
        @open="idea = $event"
        @approve="approveIdea"
        @reject="rejectIdeaItem = $event"
      />

      <Rejected
        v-else-if="tab === 'rejected' && canModerate"
        :ideas="rejectedIdeas"
        @open="idea = $event"
        @approve="approveIdea"
        @remove="askDeleteIdea"
      />

      <Members
        v-else-if="tab === 'members' && isAdmin"
        :board-id="board.id"
        :members="board.members"
        @add="addMember(board.id, $event)"
        @remove="removeMember(board.id, $event)"
        @role="toggleModerator(board.id, $event)"
        @open-member="profileUser = $event"
      />

      <Settings
        v-else-if="tab === 'settings' && isAdmin"
        :board="board"
        :saved="settingsSaved"
        @save="saveSettings"
        @transfer-admin="transferAdmin(board.id, $event)"
      />
    </section>

    <IdeaForm
      v-if="ideaOpen"
      :allow-anonymous="board.allowAnonymous"
      @close="ideaOpen = false"
      @save="saveIdea"
    />

    <IdeaInfo v-if="idea" :idea="idea" @close="idea = null" />

    <RejectModal
      v-if="rejectIdeaItem"
      :idea="rejectIdeaItem"
      @close="rejectIdeaItem = null"
      @confirm="saveReject"
    />

    <ExportModal v-if="exportOpen" :ideas="voteResults" :board="board" @close="exportOpen = false" />
    <AiModal v-if="aiOpen" :ideas="voteResults" :board="board" @close="aiOpen = false" />
    <UserInfoModal v-if="profileUser" :user="profileUser" @close="profileUser = null" />
    <VotingCreateModal
      v-if="votingCreateOpen"
      @close="votingCreateOpen = false"
      @create="saveVoting"
    />
    <ConfirmModal
      v-if="confirm"
      :title="confirm.title"
      :text="confirm.text"
      :confirm-text="confirm.confirmText"
      @cancel="confirm = null"
      @confirm="confirm.action"
    />
  </main>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import Ideas from '../features/ideas/Ideas.vue'
import IdeaForm from '../features/ideas/IdeaForm.vue'
import IdeaInfo from '../features/ideas/IdeaInfo.vue'
import Voting from '../features/voting/Voting.vue'
import VotingCreateModal from '../features/voting/VotingCreateModal.vue'
import Moderation from '../features/moderation/Moderation.vue'
import Rejected from '../features/moderation/Rejected.vue'
import RejectModal from '../features/moderation/RejectModal.vue'
import Members from '../features/members/Members.vue'
import Settings from '../features/settings/Settings.vue'
import ExportModal from '../features/export/ExportModal.vue'
import AiModal from '../features/ai/AiModal.vue'
import UserInfoModal from '../features/profile/UserInfoModal.vue'
import ConfirmModal from '../components/ui/ConfirmModal.vue'
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
  state,
} = useStore()

const tab = ref('ideas')
const ideaOpen = ref(false)
const exportOpen = ref(false)
const aiOpen = ref(false)
const votingCreateOpen = ref(false)
const idea = ref(null)
const rejectIdeaItem = ref(null)
const profileUser = ref(null)
const settingsSaved = ref(false)
const confirm = ref(null)

const navItems = [
  { id: 'ideas', title: 'Идеи' },
  { id: 'voting', title: 'Голоса' },
  { id: 'moderation', title: 'Модерация', minRole: 'moderator' },
  { id: 'rejected', title: 'Отклоненные', minRole: 'moderator' },
  { id: 'members', title: 'Участники', minRole: 'admin' },
  { id: 'settings', title: 'Настройки', minRole: 'admin' },
]

const board = computed(() => getBoard(props.boardId) || { members: [] })
const role = computed(() => board.value.role || 'member')
const isAdmin = computed(() => role.value === 'admin')
const canModerate = computed(() => ['admin', 'moderator'].includes(role.value))
const currentUsername = computed(() => state.auth.user?.username || '')
const sections = computed(() =>
  navItems.filter((section) => {
    if (section.minRole === 'admin') return isAdmin.value
    if (section.minRole === 'moderator') return canModerate.value
    return true
  })
)
const ideas = computed(() => getBoardIdeas(props.boardId))
const approvedIdeas = computed(() => ideas.value.filter((idea) => idea.status === 'approved'))
const pendingIdeas = computed(() => ideas.value.filter((idea) => idea.status === 'pending'))
const rejectedIdeas = computed(() => ideas.value.filter((idea) => idea.status === 'rejected'))
const voteResults = computed(() => getVoteResults(props.boardId))
const tabTitle = computed(() => sections.value.find((section) => section.id === tab.value)?.title || 'Доска')

onMounted(loadData)
watch(() => props.boardId, loadData)
watch(sections, (items) => {
  if (!items.some((item) => item.id === tab.value)) {
    tab.value = items[0]?.id || 'ideas'
  }
})

async function loadData() {
  const loadedBoard = await loadBoard(props.boardId)
  await loadIdeas(props.boardId)
  if (['admin', 'moderator'].includes(loadedBoard.role)) {
    await loadModerationIdeas(props.boardId).catch(() => [])
  }
  await loadVotings(props.boardId).catch(() => [])
  connectIdeasWs(props.boardId)
}

async function saveIdea(form) {
  await createIdea(props.boardId, form)
  ideaOpen.value = false
}

async function saveVoting(type) {
  await createVoting(props.boardId, type)
  votingCreateOpen.value = false
}

function askDeleteIdea(ideaId) {
  confirm.value = {
    title: 'Удалить идею?',
    text: 'Идея удалится без восстановления. Точно удалить?',
    confirmText: 'удалить идею',
    action: async () => {
      await deleteIdea(ideaId)
      confirm.value = null
    },
  }
}

function askDeleteVoting(votingId) {
  confirm.value = {
    title: 'Удалить голосование?',
    text: 'Голоса и результаты этого голосования будут удалены. Точно удалить?',
    confirmText: 'удалить голосование',
    action: async () => {
      await deleteVoting(props.boardId, votingId)
      confirm.value = null
    },
  }
}

async function saveReject(ideaId, reason) {
  await rejectIdea(ideaId, reason)
  rejectIdeaItem.value = null
}

async function saveSettings(form) {
  await updateBoard(props.boardId, form)
  settingsSaved.value = true
  window.setTimeout(() => {
    settingsSaved.value = false
  }, 2200)
}

function openIdeaAuthor(idea) {
  const member = board.value.members.find((item) => item.username === idea.authorUsername)
  profileUser.value = member || {
    username: idea.authorUsername,
    name: idea.authorName || idea.author,
  }
}
</script>
