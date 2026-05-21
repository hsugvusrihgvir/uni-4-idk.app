<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">СѓС‡Р°СЃС‚РЅРёРєРё</p>
        <h2>РџСЂРёРіР»Р°С€РµРЅРёСЏ Рё СЂРѕР»Рё</h2>
      </div>
    </header>

    <form class="inline-form" @submit.prevent="submit">
      <input v-model="username" placeholder="username" />
      <button class="button primary">РїСЂРёРіР»Р°СЃРёС‚СЊ</button>
    </form>

    <section class="invite-panel">
      <div>
        <h3>РЎСЃС‹Р»РєР° РїСЂРёРіР»Р°С€РµРЅРёСЏ</h3>
        <p>https://invite.local/board/{{ boardId }}</p>
      </div>
      <div class="qr-box">QR</div>
    </section>

    <div class="row-list">
      <article v-for="member in members" :key="member.id" class="member-card">
        <div class="member-avatar">{{ (member.name || member.username).slice(0, 1) }}</div>
        <div class="member-info">
          <h3>{{ member.name || member.username }}</h3>
          <p>{{ member.username }} / {{ member.role }}</p>
        </div>

        <div class="member-actions">
          <button class="button ghost" :disabled="member.role === 'admin'" @click="$emit('role', member.id)">
            СЂРѕР»СЊ
          </button>
          <button class="text-danger" :disabled="member.role === 'admin'" @click="$emit('remove', member.id)">
            СѓРґР°Р»РёС‚СЊ
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
const username = ref('')

function submit() {
  emit('add', username.value)
  username.value = ''
}
</script>
