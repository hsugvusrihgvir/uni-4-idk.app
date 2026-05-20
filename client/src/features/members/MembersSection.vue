<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">участники</p>
        <h2>Приглашения и роли</h2>
      </div>
    </header>

    <form class="inline-form" @submit.prevent="submit">
      <input v-model="name" placeholder="ник участника" />
      <button class="button primary">пригласить</button>
    </form>

    <section class="invite-panel">
      <div>
        <h3>Ссылка приглашения</h3>
        <p>https://invite.local/board/{{ boardId }}</p>
      </div>
      <div class="qr-box">QR</div>
    </section>

    <div class="row-list">
      <article v-for="member in members" :key="member.id" class="member-card">
        <div class="member-avatar">{{ member.name.slice(0, 1) }}</div>
        <div class="member-info">
          <h3>{{ member.name }}</h3>
          <p>{{ member.role }}</p>
        </div>

        <div class="member-actions">
          <button
            class="button ghost"
            :disabled="member.role === 'Админ'"
            @click="$emit('role', member.id)"
          >
            роль
          </button>
          <button
            class="text-danger"
            :disabled="member.role === 'Админ'"
            @click="$emit('remove', member.id)"
          >
            удалить
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  members: { type: Array, default: () => [] },
  boardId: { type: String, required: true },
})

const emit = defineEmits(['add', 'remove', 'role'])
const name = ref('')

function submit() {
  emit('add', name.value)
  name.value = ''
}
</script>
