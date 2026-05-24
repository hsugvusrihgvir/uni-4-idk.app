<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">настройки</p>
        <h2>Описание и параметры доски</h2>
      </div>
    </header>

    <form class="settings-grid" @submit.prevent="save">
      <label class="field">
        Название доски
        <input v-model="form.title" />
      </label>

      <label class="field span-2">
        Описание
        <textarea v-model="form.description"></textarea>
      </label>

      <label class="field span-2">
        Контекст доски
        <textarea v-model="form.context"></textarea>
      </label>

      <label class="checkbox-field">
        <input v-model="form.allowAnonymous" type="checkbox" />
        разрешить анонимные идеи
      </label>

      <label class="checkbox-field">
        <input v-model="form.autoApprove" type="checkbox" />
        сразу одобрять новые идеи
      </label>

      <button class="button primary">сохранить</button>
    </form>

    <section class="transfer-panel">
      <h3>Передача прав администратора</h3>
      <p>На доске всегда должен быть хотя бы один администратор.</p>

      <select v-model="newAdminId">
        <option v-for="member in board.members" :key="member.id" :value="member.id">
          {{ member.name }} — {{ member.role }}
        </option>
      </select>

      <button class="button ghost" @click="$emit('transfer-admin', newAdminId)">
        передать права
      </button>
    </section>
  </section>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'

const props = defineProps({
  board: { type: Object, required: true },
})

const emit = defineEmits(['save', 'transfer-admin'])

const form = reactive({
  title: props.board.title,
  description: props.board.description,
  context: props.board.context,
  allowAnonymous: props.board.allowAnonymous,
  autoApprove: props.board.autoApprove,
})

const newAdminId = ref(props.board.members.find((m) => m.role === 'admin')?.id)

watch(
  () => props.board,
  (board) => {
    form.title = board.title
    form.description = board.description
    form.context = board.context
    form.allowAnonymous = board.allowAnonymous
    form.autoApprove = board.autoApprove
    newAdminId.value = board.members.find((m) => m.role === 'admin')?.id
  },
  { deep: true }
)

function save() {
  emit('save', { ...form })
}
</script>
