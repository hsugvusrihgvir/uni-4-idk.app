<template>
  <Modal title="Профиль" label="участник" @close="$emit('close')">
    <section class="profile-view">
      <span class="avatar-preview profile-avatar">
        <img v-if="user.photoUrl" :src="user.photoUrl" alt="avatar" />
        <span v-else>{{ avatarLetter }}</span>
      </span>

      <div>
        <h2>{{ user.name || user.username }}</h2>
        <p v-if="user.username">@{{ user.username }}</p>
        <p v-if="user.role" class="chip">{{ user.role }}</p>
      </div>

      <button class="button primary" type="button" @click="$emit('close')">закрыть</button>
    </section>
  </Modal>
</template>

<script setup>
import { computed } from 'vue'
import Modal from '../../components/ui/Modal.vue'

const props = defineProps({
  user: { type: Object, required: true },
})

defineEmits(['close'])

const avatarLetter = computed(() => (props.user.name || props.user.username || '?').slice(0, 1).toUpperCase())
</script>
