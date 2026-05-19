<template>
  <form class="auth-card" @submit.prevent="submit">
    <p class="eyebrow">idk.app</p>
    <h1>Вход</h1>

    <label class="field">
      Email
      <input v-model="form.email" type="email" placeholder="name@example.com" />
    </label>

    <label class="field">
      Код
      <input v-model="form.code" placeholder="1234" />
    </label>

    <button class="button primary">Войти</button>
  </form>
</template>

<script setup>
import { reactive } from 'vue'

const emit = defineEmits(['submit'])

const form = reactive({
  email: '',
  code: '',
})

function submit() {
  emit('submit', { email: form.email, code: form.code })
}
</script>
