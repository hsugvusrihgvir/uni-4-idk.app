<template>
  <Modal title="Экспорт идей" label="txt" @close="$emit('close')">
    <div class="modal-form">
      <label class="field">
        Минимальный процент одобрения
        <input v-model.number="threshold" type="number" min="0" max="100" />
      </label>

      <button class="button primary" @click="download">скачать файл</button>
    </div>
  </Modal>
</template>

<script setup>
import { ref } from 'vue'
import Modal from '../../components/ui/Modal.vue'

const props = defineProps({
  ideas: { type: Array, default: () => [] },
})

defineEmits(['close'])

const threshold = ref(50)

function download() {
  const text = props.ideas
    .filter((idea) => idea.approvalPercent >= threshold.value)
    .map((idea) => `${idea.title}\n${idea.description}\nОдобрение: ${idea.approvalPercent}%\n`)
    .join('\n')

  const blob = new Blob([text || 'Нет идей для экспорта'], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'ideas.txt'
  link.click()
  URL.revokeObjectURL(url)
}
</script>
