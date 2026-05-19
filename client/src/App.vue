<template>
  <div class="app-shell">
    <DecorBackground />

    <AuthPage v-if="currentPage === 'auth'" @login="handleLogin" />

    <BoardsPage
      v-else-if="currentPage === 'boards'"
      @open-board="openBoard"
      @logout="currentPage = 'auth'"
    />

    <BoardPage
      v-else
      :board-id="activeBoardId"
      @back="currentPage = 'boards'"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DecorBackground from './components/ui/DecorBackground.vue'
import AuthPage from './pages/AuthPage.vue'
import BoardsPage from './pages/BoardsPage.vue'
import BoardPage from './pages/BoardPage.vue'
import { useAppStore } from './store/useAppStore'

const { login } = useAppStore()

const currentPage = ref('auth')
const activeBoardId = ref(null)

function handleLogin(payload) {
  login(payload)
  currentPage.value = 'boards'
}

function openBoard(boardId) {
  activeBoardId.value = boardId
  currentPage.value = 'board'
}
</script>
