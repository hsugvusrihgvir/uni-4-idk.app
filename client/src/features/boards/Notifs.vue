<template>
  <aside class="notifications-panel">
    <header class="modal-header">
      <div>
        <p class="eyebrow">СѓРІРµРґРѕРјР»РµРЅРёСЏ</p>
        <h3>РЎРѕР±С‹С‚РёСЏ</h3>
      </div>
      <button class="round-button" @click="$emit('close')">Г—</button>
    </header>

    <div class="notification-list">
      <article v-for="notif in notifications" :key="notif.id" class="notification-item">
        <p>{{ notif.text }}</p>
        <small>{{ notif.createdAt }}</small>
        <button class="text-danger" @click="$emit('remove', notif.id)">СѓРґР°Р»РёС‚СЊ</button>
      </article>

      <p v-if="!notifications.length">РџРѕРєР° РЅРµС‚ СѓРІРµРґРѕРјР»РµРЅРёР№.</p>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  notifications: { type: Array, default: () => [] },
})

defineEmits(['close', 'remove'])
</script>
