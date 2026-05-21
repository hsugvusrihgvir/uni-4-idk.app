<template>
  <div class="app-shell">
    <Bg />

    <Auth v-if="page === 'auth'" @authenticated="page = 'boards'" />

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
import { ref } from 'vue'
import Bg from './components/ui/Bg.vue'
import Auth from './pages/Auth.vue'
import Boards from './pages/Boards.vue'
import Board from './pages/Board.vue'
import { useStore } from './store/store'

const { logout } = useStore()

const page = ref('auth')
const boardId = ref(null)

function openBoard(id) {
  boardId.value = id
  page.value = 'board'
}

function exit() {
  logout()
  page.value = 'auth'
}
</script>
