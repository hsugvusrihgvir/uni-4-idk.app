<template>
  <Modal title="ИИ-сводка" label="макет функции" wide @close="$emit('close')">
    <div class="modal-form">
      <p class="muted">
        Это локальная имитация: выбранные идеи объединяются в один текст без запроса к API.
      </p>

      <label class="field">
        Минимальный процент одобрения
        <input v-model.number="threshold" type="number" min="0" max="100" />
      </label>

      <button class="button primary" @click="generate">собрать текст</button>

      <pre v-if="summary" class="summary-box">{{ summary }}</pre>
    </div>
  </Modal>
</template>

<script setup>
import { ref } from 'vue'
import Modal from '../../components/ui/Modal.vue'

const props = defineProps({
  ideas: { type: Array, default: () => [] },
  board: { type: Object, required: true },
})

defineEmits(['close'])

const threshold = ref(50)
const summary = ref('')

function generate() {
  const selected = props.ideas.filter((idea) => idea.approvalPercent >= threshold.value)
  if (!selected.length) {
    summary.value = 'Нет идей, подходящих под выбранный порог.'
    return
  }

  summary.value = [
    `Контекст: ${props.board.context || props.board.description}`,
    '',
    'Итоговый текст:',
    selected.map((idea) => idea.description).join(' '),
  ].join('\n')
}
</script>
