<template>
  <Modal title="Создать голосование" label="тип голосования" @close="$emit('close')">
    <div class="modal-form">
      <div class="voting-type-list">
        <button
          v-for="type in types"
          :key="type.id"
          class="voting-type-card"
          type="button"
          @click="$emit('create', type.id)"
        >
          <span class="voting-type-icon">{{ type.icon }}</span>
          <span>
            <strong>{{ type.title }}</strong>
            <small>{{ type.text }}</small>
          </span>
        </button>
      </div>
    </div>
  </Modal>
</template>

<script setup>
import Modal from '../../components/ui/Modal.vue'

defineEmits(['create', 'close'])

const types = [
  {
    id: 'yes_no',
    icon: '1',
    title: 'Один выбор',
    text: 'Участник может выбрать только одну идею. Новый голос заменит старый.',
  },
  {
    id: 'like',
    icon: '+',
    title: 'Несколько идей',
    text: 'Участник может поддержать сколько угодно идей и отменить любой голос.',
  },
]
</script>
