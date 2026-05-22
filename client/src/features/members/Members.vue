<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">участники</p>
        <h2>Приглашения и роли</h2>
      </div>
    </header>

    <form class="inline-form" @submit.prevent="submit">
      <input v-model="username" placeholder="username" />
      <button class="button primary">пригласить</button>
    </form>

    <section class="invite-panel">
      <div>
        <h3>Ссылка приглашения</h3>
        <p>{{ inviteLink }}</p>
      </div>
      <img v-if="qrUrl" class="qr-box" :src="qrUrl" alt="qr invite" />
    </section>

    <div class="row-list">
      <article v-for="member in members" :key="member.id" class="member-card">
        <div class="member-avatar">
          <img v-if="member.photoUrl" :src="member.photoUrl" alt="avatar" />
          <span v-else>{{ (member.name || member.username).slice(0, 1) }}</span>
        </div>
        <div class="member-info">
          <h3>{{ member.name || member.username }}</h3>
          <p>{{ member.username }} / {{ member.role }}</p>
        </div>

        <div class="member-actions">
          <button class="button ghost" :disabled="member.role === 'admin'" @click="$emit('role', member.id)">
            роль
          </button>
          <button class="text-danger" :disabled="member.role === 'admin'" @click="$emit('remove', member.id)">
            удалить
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, watchEffect } from 'vue'
import QRCode from 'qrcode'

const props = defineProps({
  members: { type: Array, default: () => [] },
  boardId: { type: String, required: true },
})

const emit = defineEmits(['add', 'remove', 'role'])
const username = ref('')
const qrUrl = ref('')
const inviteLink = computed(() => `${window.location.origin}/invite/${props.boardId}`)

watchEffect(async () => {
  qrUrl.value = await QRCode.toDataURL(inviteLink.value, {
    width: 180,
    margin: 2,
    color: {
      dark: '#4d3140',
      light: '#ffffff',
    },
  })
})

function submit() {
  emit('add', username.value)
  username.value = ''
}
</script>
