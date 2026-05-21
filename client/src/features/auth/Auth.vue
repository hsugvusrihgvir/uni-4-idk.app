<template>
  <form class="auth-card" novalidate @submit.prevent="submit">
    <p class="eyebrow">idk.app</p>
    <h1>{{ title }}</h1>

    <p v-if="message" class="form-message success">{{ message }}</p>
    <p v-if="error" class="form-message error">{{ error }}</p>

    <template v-if="step === 'email'">
      <label class="field">
        Email
        <input v-model.trim="form.email" type="text" inputmode="email" placeholder="name@example.com" />
      </label>
    </template>

    <template v-else-if="step === 'register'">
      <label class="field">
        Email
        <input v-model.trim="form.email" type="text" inputmode="email" placeholder="name@example.com" />
      </label>

      <label class="field">
        Username
        <input v-model.trim="form.username" placeholder="username" @blur="checkName" />
      </label>

      <p v-if="usernameMessage" class="form-message success">{{ usernameMessage }}</p>

      <label class="field">
        {{ ui.name }}
        <input v-model.trim="form.name" placeholder="Name" />
      </label>

      <label class="field">
        {{ ui.photo }}
        <input v-model.trim="form.photo_url" placeholder="photo.png" />
      </label>
    </template>

    <template v-else>
      <label class="field">
        Email
        <input v-model.trim="form.email" type="text" inputmode="email" placeholder="name@example.com" />
      </label>

      <label class="field">
        {{ ui.code }}
        <input v-model.trim="form.code" inputmode="numeric" placeholder="123456" />
      </label>
    </template>

    <div class="auth-actions">
      <button v-if="step !== 'email'" class="button ghost" type="button" @click="back">{{ ui.back }}</button>
      <button class="button primary" :disabled="loading">{{ buttonText }}</button>
    </div>
  </form>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useStore } from '../../store/store.js'

const emit = defineEmits(['authenticated'])
const { state, requestLogin, registerUser, verifyLogin, checkUsername } = useStore()

const step = ref('email')
const error = ref('')
const message = ref('')
const usernameMessage = ref('')

const ui = {
  name: '\u0418\u043c\u044f',
  photo: '\u0424\u043e\u0442\u043e',
  code: '\u041a\u043e\u0434',
  back: '\u043d\u0430\u0437\u0430\u0434',
}

const text = {
  enterEmail: '\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043d\u0443\u044e \u043f\u043e\u0447\u0442\u0443, \u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440 name@example.com',
  enterEmailShort: '\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043d\u0443\u044e \u043f\u043e\u0447\u0442\u0443.',
  codeSent: '\u041a\u043e\u0434 \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d. \u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0435\u0433\u043e \u043d\u0438\u0436\u0435.',
  needRegister: 'Аккаунт не найден. Зарегистрируйтесь, чтобы продолжить.',
  usernameShort: 'Username \u0434\u043e\u043b\u0436\u0435\u043d \u0431\u044b\u0442\u044c \u043d\u0435 \u043a\u043e\u0440\u043e\u0447\u0435 3 \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432.',
  usernameTaken: 'Username \u0443\u0436\u0435 \u0437\u0430\u043d\u044f\u0442.',
  usernameFree: 'Username \u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d.',
  registered: '\u0410\u043a\u043a\u0430\u0443\u043d\u0442 \u0441\u043e\u0437\u0434\u0430\u043d. \u041a\u043e\u0434 \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d, \u0432\u0432\u0435\u0434\u0438\u0442\u0435 \u0435\u0433\u043e \u043d\u0438\u0436\u0435.',
  enterCode: '\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043e\u0434 \u0438\u0437 \u043f\u0438\u0441\u044c\u043c\u0430.',
}

const form = reactive({
  email: '',
  username: '',
  name: '',
  photo_url: '',
  code: '',
})

const loading = computed(() => state.loading)
const title = computed(() => {
  if (step.value === 'register') return '\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f'
  if (step.value === 'code') return '\u041a\u043e\u0434'
  return '\u0412\u0445\u043e\u0434'
})

const buttonText = computed(() => {
  if (loading.value) return '\u0436\u0434\u0435\u043c...'
  if (step.value === 'register') return '\u0417\u0430\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c\u0441\u044f'
  if (step.value === 'code') return '\u0412\u043e\u0439\u0442\u0438'
  return '\u0414\u0430\u043b\u044c\u0448\u0435'
})

function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
}

function fail(value) {
  error.value = value
  message.value = ''
}

async function submit() {
  error.value = ''
  usernameMessage.value = ''

  if (step.value === 'email') {
    await submitEmail()
    return
  }

  if (step.value === 'register') {
    await submitRegister()
    return
  }

  await submitCode()
}

async function submitEmail() {
  if (!isEmail(form.email)) {
    fail(text.enterEmail)
    return
  }

  try {
    const exists = await requestLogin(form.email)
    step.value = exists ? 'code' : 'register'
    message.value = exists ? text.codeSent : text.needRegister
  } catch {
    fail(state.error)
  }
}

async function submitRegister() {
  if (!isEmail(form.email)) {
    fail(text.enterEmailShort)
    return
  }

  if (form.username.length < 3) {
    fail(text.usernameShort)
    return
  }

  try {
    const available = await checkUsername(form.username)
    if (!available) {
      fail(text.usernameTaken)
      return
    }

    await registerUser({
      email: form.email,
      username: form.username,
      name: form.name || null,
      photo_url: form.photo_url || null,
    })

    step.value = 'code'
    message.value = text.registered
  } catch {
    fail(state.error)
  }
}

async function submitCode() {
  if (form.code.length < 4) {
    fail(text.enterCode)
    return
  }

  try {
    await verifyLogin({ email: form.email, code: form.code })
    emit('authenticated')
  } catch {
    fail(state.error)
  }
}

async function checkName() {
  usernameMessage.value = ''
  if (step.value !== 'register' || form.username.length < 3) return

  try {
    const available = await checkUsername(form.username)
    usernameMessage.value = available ? text.usernameFree : ''
    if (!available) fail(text.usernameTaken)
  } catch {
    fail(state.error)
  }
}

function back() {
  step.value = 'email'
  form.code = ''
  error.value = ''
  message.value = ''
  usernameMessage.value = ''
}
</script>
