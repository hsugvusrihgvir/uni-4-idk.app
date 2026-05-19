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
      <p>Идея отклонена: причина доступна в карточке.</p>
      <p>Началось новое голосование.</p>
      <p>Вас добавили на доску.</p>
    </div>
  </aside>
</template>

<script setup>
defineEmits(['close'])
</script>
