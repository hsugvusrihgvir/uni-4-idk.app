<template>
  <main class="page">
    <section class="page-hero">
    <header class="topbar">
      <div>
        <p class="eyebrow"><h1>мои доски</h1></p>
      </div>

      <div class="topbar-actions">
        <button class="button ghost" @click="showNotifications = true">уведомления</button>
        <button class="button ghost" @click="$emit('logout')">выйти</button>
        <button class="button primary" @click="showCreateModal = true">создать доску</button>
      </div>
    </header>

    <section class="toolbar">
      <input v-model="search" placeholder="найти доску" />
    </section>
    </section>

    <section class="board-grid">
      <BoardCard
        v-for="board in filteredBoards"
        :key="board.id"
        :board="board"
        :ideas-count="getBoardIdeas(board.id).length"
        @open="$emit('open-board', $event)"
        @remove="deleteBoard"
      />
    </section>

    <EmptyState
      v-if="!filteredBoards.length"
      title="Досок нет"
      text="Создайте первую доску для сбора идей."
    />

    <BoardFormModal
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @save="handleCreateBoard"
    />

    <NotificationsPanel
      v-if="showNotifications"
      @close="showNotifications = false"
    />
  </main>
</template>

<script setup>
import { computed, ref } from 'vue'
import BoardCard from '../features/boards/BoardCard.vue'
import BoardFormModal from '../features/boards/BoardFormModal.vue'
import NotificationsPanel from '../features/boards/NotificationsPanel.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import { useAppStore } from '../store/useAppStore'

defineEmits(['open-board', 'logout'])

const { boards, createBoard, deleteBoard, getBoardIdeas, resetAll } = useAppStore()

const search = ref('')
const showCreateModal = ref(false)
const showNotifications = ref(false)

const filteredBoards = computed(() =>
  boards.value.filter((board) =>
    board.title.toLowerCase().includes(search.value.toLowerCase())
  )
)

function handleCreateBoard(payload) {
  createBoard(payload)
  showCreateModal.value = false
}
</script>
