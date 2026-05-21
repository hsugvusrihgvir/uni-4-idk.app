<template>
  <Modal title="РЎРѕР·РґР°С‚СЊ РґРѕСЃРєСѓ" label="РЅРѕРІР°СЏ РґРѕСЃРєР°" @close="$emit('close')">
    <form class="modal-form" novalidate @submit.prevent="submit">
      <p v-if="error" class="form-message error">{{ error }}</p>

      <label class="field">
        РќР°Р·РІР°РЅРёРµ
        <input v-model.trim="form.title" placeholder="Р”РѕСЃРєР° 1" />
      </label>

      <label class="field">
        РћРїРёСЃР°РЅРёРµ
        <textarea v-model.trim="form.description" placeholder="РћРїРёСЃР°РЅРёРµ РґРѕСЃРєРё"></textarea>
      </label>

      <button class="button primary">РЎРѕР·РґР°С‚СЊ</button>
    </form>
  </Modal>
</template>

<script setup>
import { reactive, ref } from 'vue'
import Modal from '../../components/ui/Modal.vue'

const emit = defineEmits(['close', 'save'])

const error = ref('')
const form = reactive({
  title: '',
  description: '',
})

function submit() {
  if (!form.title) {
    error.value = 'Р’РІРµРґРёС‚Рµ РЅР°Р·РІР°РЅРёРµ РґРѕСЃРєРё.'
    return
  }

  error.value = ''
  emit('save', { ...form })
}
</script>
