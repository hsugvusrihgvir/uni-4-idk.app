<template>
  <AppModal title="РџСЂРµРґР»РѕР¶РёС‚СЊ РёРґРµСЋ" label="РЅРѕРІР°СЏ РёРґРµСЏ" @close="$emit('close')">
    <form class="modal-form" novalidate @submit.prevent="submit">
      <p v-if="error" class="form-message error">{{ error }}</p>

      <label class="field">
        РќР°Р·РІР°РЅРёРµ
        <input v-model.trim="form.title" placeholder="РРґРµСЏ 1" />
      </label>

      <label class="field">
        РћРїРёСЃР°РЅРёРµ
        <textarea v-model.trim="form.description" placeholder="РћРїРёСЃР°РЅРёРµ РёРґРµРё"></textarea>
      </label>

      <label v-if="allowAnonymous" class="checkbox-field">
        <input v-model="form.isAnonymous" type="checkbox" />
        РѕС‚РїСЂР°РІРёС‚СЊ Р°РЅРѕРЅРёРјРЅРѕ
      </label>

      <button class="button primary">РћС‚РїСЂР°РІРёС‚СЊ</button>
    </form>
  </AppModal>
</template>

<script setup>
import { reactive, ref } from 'vue'
import AppModal from '../../components/ui/AppModal.vue'

defineProps({
  allowAnonymous: { type: Boolean, default: true },
})

const emit = defineEmits(['close', 'save'])

const error = ref('')
const form = reactive({
  title: '',
  description: '',
  isAnonymous: true,
})

function submit() {
  if (!form.title) {
    error.value = 'Р’РІРµРґРёС‚Рµ РЅР°Р·РІР°РЅРёРµ РёРґРµРё.'
    return
  }

  if (!form.description) {
    error.value = 'Р’РІРµРґРёС‚Рµ РѕРїРёСЃР°РЅРёРµ РёРґРµРё.'
    return
  }

  error.value = ''
  emit('save', { ...form })
}
</script>
