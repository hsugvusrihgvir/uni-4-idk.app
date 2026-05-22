<template>
  <div class="app-shell">
    <Bg />

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
import { onMounted, ref } from 'vue'
import Bg from './components/ui/Bg.vue'
import Auth from './pages/Auth.vue'
import Boards from './pages/Boards.vue'
import Board from './pages/Board.vue'
import { useStore } from './store/store'

const { state, logout, joinBoard } = useStore()

const page = ref('auth')
const boardId = ref(null)
const inviteId = ref(getInviteId())

onMounted(async () => {
  if (inviteId.value && state.auth.accessToken) await acceptInvite()
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
</script>
