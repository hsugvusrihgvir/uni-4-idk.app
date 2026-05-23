<template>
  <main class="page">
    <section class="page-hero">
      <header class="topbar">
        <div>
          <p class="eyebrow"><h1>Мои доски</h1></p>
        </div>

        <div class="topbar-actions">
          <button class="button ghost profile-button" @click="profileOpen = true">
            <span class="member-avatar small-avatar">
              <img v-if="currentUser?.photoUrl" :src="currentUser.photoUrl" alt="avatar" />
              <span v-else>{{ avatarLetter }}</span>
            </span>
            профиль
          </button>
          <button class="button ghost" @click="openNotifs">уведомления</button>
          <button class="button ghost" @click="$emit('logout')">выйти</button>
          <button class="button primary" @click="formOpen = true">создать доску</button>
        </div>
      </header>

      <section class="toolbar">
        <input v-model="search" placeholder="найти доску" />
      </section>
    </section>

    <section class="board-grid">
      <BoardCard
        v-for="board in foundBoards"
        :key="board.id"
        :board="board"
        :ideas-count="getBoardIdeas(board.id).length"
        @open="$emit('open-board', $event)"
        @remove="deleteBoard"
      />
    </section>

    <Empty
      v-if="!foundBoards.length"
      title="Досок нет"
      text="Создайте первую доску для сбора идей."
    />

    <BoardForm v-if="formOpen" @close="formOpen = false" @save="saveBoard" />

    <ProfileModal v-if="profileOpen" @close="profileOpen = false" />

    <Notifs
      v-if="notifsOpen"
      :notifications="notifications"
      @close="notifsOpen = false"
      @remove="deleteNotification"
    />
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import BoardCard from '../features/boards/BoardCard.vue'
import BoardForm from '../features/boards/BoardForm.vue'
import Notifs from '../features/boards/Notifs.vue'
import ProfileModal from '../features/profile/ProfileModal.vue'
import Empty from '../components/ui/Empty.vue'
import { useStore } from '../store/store'
import { fileUrl } from '../api/users.js'

defineEmits(['open-board', 'logout'])

const {
  boards,
  state,
  notifications,
  loadBoards,
  createBoard,
  deleteBoard,
  getBoardIdeas,
  loadNotifications,
  deleteNotification,
} = useStore()

const search = ref('')
const formOpen = ref(false)
const notifsOpen = ref(false)
const profileOpen = ref(false)

const currentUser = computed(() => {
  const user = state.auth.user
  if (!user) return null
  return { ...user, photoUrl: fileUrl(user.photo_url) }
})

const avatarLetter = computed(() =>
  (currentUser.value?.name || currentUser.value?.username || '?').slice(0, 1).toUpperCase()
)

const foundBoards = computed(() =>
  boards.value.filter((board) => board.title.toLowerCase().includes(search.value.toLowerCase()))
)

onMounted(loadBoards)

async function openNotifs() {
  await loadNotifications()
  notifsOpen.value = true
}

async function saveBoard(form) {
  await createBoard(form)
  formOpen.value = false
}
</script>
