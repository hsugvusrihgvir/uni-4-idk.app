<template>
  <div class="app-shell">
    <Bg />

    <button
      class="theme-toggle"
      type="button"
      :aria-pressed="theme === 'dark'"
      @click="toggleTheme"
    >
      {{ theme === 'dark' ? 'светлая' : 'темная' }}
    </button>

    <Auth v-if="page === 'auth'" @authenticated="afterAuth" />

    <Boards
      v-else-if="page === 'boards'"
      @open-board="openBoard"
      @logout="exit"
    />

    <Board
      v-else
      :board-id="boardId"
      @back="page = 'boards'"
    />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import Bg from './components/ui/Bg.vue'
import Auth from './pages/Auth.vue'
import Boards from './pages/Boards.vue'
import Board from './pages/Board.vue'
import { useStore } from './store/store'

const { state, logout, joinBoard, loadProfile, loadBoards } = useStore()

const page = ref('auth')
const boardId = ref(null)
const inviteId = ref(getInviteId())
const theme = ref(localStorage.getItem('theme') || 'light')

watch(theme, (value) => {
  document.documentElement.dataset.theme = value
  localStorage.setItem('theme', value)
}, { immediate: true })

onMounted(async () => {
  if (!state.auth.accessToken) return

  try {
    await loadProfile()
    await loadBoards()

    if (inviteId.value) {
      await acceptInvite()
      return
    }

    page.value = 'boards'
  } catch {
    exit()
  }
})

function getInviteId() {
  const match = window.location.pathname.match(/^\/invite\/([^/]+)$/)
  return match?.[1] || null
}

function openBoard(id) {
  boardId.value = id
  page.value = 'board'
}

async function acceptInvite() {
  const board = await joinBoard(inviteId.value)
  window.history.replaceState({}, '', '/')
  inviteId.value = null
  openBoard(board.id)
}

async function afterAuth() {
  if (inviteId.value) {
    await acceptInvite()
    return
  }

  page.value = 'boards'
}

function exit() {
  logout()
  page.value = 'auth'
}

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
}
</script>
