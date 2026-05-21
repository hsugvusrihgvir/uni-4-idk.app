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
        <span class="avatar-upload">
          <span class="avatar-preview">
            <img v-if="avatarUrl" :src="avatarUrl" alt="avatar" />
            <span v-else>{{ avatarLetter }}</span>
          </span>
          <span class="button ghost file-button">выбрать фото</span>
          <input type="file" accept="image/png,image/jpeg,image/webp" @change="pickAvatar" />
        </span>
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
const { state, requestLogin, registerUser, verifyLogin, checkUsername, uploadAvatar } = useStore()

const step = ref('email')
const error = ref('')
const message = ref('')
const usernameMessage = ref('')
const avatar = ref(null)
const avatarUrl = ref('')

const ui = {
  name: 'Имя',
  photo: 'Фото',
  code: 'Код',
  back: 'назад',
}

const text = {
  enterEmail: 'Введите корректную почту, например name@example.com',
  enterEmailShort: 'Введите корректную почту.',
  codeSent: 'Код отправлен. Введите его ниже.',
  needRegister: 'Аккаунт не найден. Зарегистрируйтесь, чтобы продолжить.',
  usernameShort: 'Username должен быть не короче 3 символов.',
  usernameTaken: 'Username уже занят.',
  usernameFree: 'Username доступен.',
  registered: 'Аккаунт создан. Код отправлен, введите его ниже.',
  enterCode: 'Введите код из письма.',
  badPhoto: 'Выберите картинку png, jpg или webp.',
}

const form = reactive({
  email: '',
  username: '',
  name: '',
  code: '',
})

const loading = computed(() => state.loading)
const avatarLetter = computed(() => (form.name || form.username || '?').slice(0, 1).toUpperCase())
const title = computed(() => {
  if (step.value === 'register') return 'Регистрация'
  if (step.value === 'code') return 'Код'
  return 'Вход'
})

const buttonText = computed(() => {
  if (loading.value) return 'ждем...'
  if (step.value === 'register') return 'Зарегистрироваться'
  if (step.value === 'code') return 'Войти'
  return 'Дальше'
})

function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
}

function fail(value) {
  error.value = value
  message.value = ''
}

function imageFile(file) {
  return file && ['image/jpeg', 'image/png', 'image/webp'].includes(file.type)
}

function readImage(file) {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => resolve(img)
    img.onerror = reject
    img.src = URL.createObjectURL(file)
  })
}

async function resizeAvatar(file) {
  const img = await readImage(file)
  const size = Math.min(img.width, img.height)
  const left = (img.width - size) / 2
  const top = (img.height - size) / 2
  const canvas = document.createElement('canvas')
  canvas.width = 256
  canvas.height = 256
  canvas.getContext('2d').drawImage(img, left, top, size, size, 0, 0, 256, 256)

  return new Promise((resolve) => {
    canvas.toBlob((blob) => resolve(new File([blob], 'avatar.jpg', { type: 'image/jpeg' })), 'image/jpeg', 0.82)
  })
}

async function pickAvatar(event) {
  const file = event.target.files?.[0]
  if (!file) return

  if (!imageFile(file)) {
    fail(text.badPhoto)
    return
  }

  avatar.value = await resizeAvatar(file)
  if (avatarUrl.value) URL.revokeObjectURL(avatarUrl.value)
  avatarUrl.value = URL.createObjectURL(avatar.value)
  error.value = ''
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

    const photoUrl = avatar.value ? await uploadAvatar(avatar.value) : null
    await registerUser({
      email: form.email,
      username: form.username,
      name: form.name || null,
      photo_url: photoUrl,
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
