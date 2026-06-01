<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">настройки</p>
        <h2>Описание и параметры доски</h2>
      </div>
    </header>

    <form class="settings-grid" @submit.prevent="save">
      <p v-if="saved" class="form-message success span-2">Настройки сохранены.</p>

      <label class="field">
        Название доски
        <input v-model="form.title" />
      </label>

      <label class="field span-2">
        Описание
        <textarea v-model="form.description"></textarea>
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

    <section class="telegram-panel">
      <div>
        <h3>Telegram-чат</h3>
        <p>Добавьте бота в общий чат и отправьте эту команду. Писать должен админ доски.</p>
        <a class="telegram-link" href="https://t.me/idkapp_bot" target="_blank" rel="noopener noreferrer">
          @idkapp_bot
        </a>
      </div>

      <div class="code-box">{{ bindCommand }}</div>

      <button class="button ghost" type="button" @click="copyBindCommand">
        {{ copied ? 'скопировано' : 'скопировать команду' }}
      </button>
      <p v-if="copyError" class="form-message error">{{ copyError }}</p>
    </section>

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
import { computed, reactive, ref, watch } from 'vue'

const props = defineProps({
  board: { type: Object, required: true },
  saved: { type: Boolean, default: false },
})

const emit = defineEmits(['save', 'transfer-admin'])

const form = reactive({
  title: props.board.title,
  description: props.board.description,
  allowAnonymous: props.board.allowAnonymous,
  autoApprove: props.board.autoApprove,
})

const newAdminId = ref(props.board.members.find((m) => m.role === 'admin')?.id)
const copied = ref(false)
const copyError = ref('')
const bindCommand = computed(() => `/bind ${props.board.id}`)

watch(
  () => props.board,
  (board) => {
    form.title = board.title
    form.description = board.description
    form.allowAnonymous = board.allowAnonymous
    form.autoApprove = board.autoApprove
    newAdminId.value = board.members.find((m) => m.role === 'admin')?.id
  },
  { deep: true }
)

function save() {
  emit('save', { ...form })
}

async function copyBindCommand() {
  copyError.value = ''

  try {
    if (!navigator.clipboard) throw new Error()
    await navigator.clipboard.writeText(bindCommand.value)
    copied.value = true
    window.setTimeout(() => {
      copied.value = false
    }, 1800)
  } catch {
    copyError.value = 'не получилось скопировать, выделите команду вручную'
  }
}
</script>
