<template>
  <aside class="notifications-panel">
    <header class="modal-header">
      <div>
        <p class="eyebrow">уведомления</p>
        <h3>События</h3>
      </div>
      <button class="round-button" @click="$emit('close')">×</button>
    </header>

    <div class="notification-list">
      <article v-for="notif in notifications" :key="notif.id" class="notification-item">
        <p>{{ notif.text }}</p>
        <small>{{ notif.createdAt }}</small>
        <button class="text-danger" @click="$emit('remove', notif.id)">удалить</button>
      </article>

      <p v-if="!notifications.length">Пока нет уведомлений.</p>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  notifications: { type: Array, default: () => [] },
})

defineEmits(['close', 'remove'])
</script>
