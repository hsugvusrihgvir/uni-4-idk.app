<template>
  <Modal title="Профиль" label="аккаунт" @close="$emit('close')">
    <form class="profile-form" @submit.prevent="save">
      <p v-if="message" class="form-message success">{{ message }}</p>
      <p v-if="error" class="form-message error">{{ error }}</p>

      <div class="profile-head">
        <span class="avatar-preview profile-avatar">
          <img v-if="previewUrl" :src="previewUrl" alt="avatar" />
          <span v-else>{{ avatarLetter }}</span>
        </span>

        <label class="button ghost file-button">
          выбрать фото
          <input type="file" accept="image/png,image/jpeg,image/webp" @change="pickAvatar" />
        </label>
      </div>

      <label class="field">
        Email
        <input v-model="form.email" disabled />
      </label>

      <label class="field">
        Username
        <input v-model.trim="form.username" placeholder="username" @blur="checkName" />
      </label>

      <p v-if="usernameMessage" class="form-message success">{{ usernameMessage }}</p>

      <label class="field">
        Имя
        <input v-model.trim="form.name" placeholder="Имя" />
      </label>

      <section class="telegram-panel">
        <div>
          <h3>Telegram</h3>
          <p v-if="form.tg_id">аккаунт уже привязан</p>
          <p v-else>Получите код и отправьте его боту командой `/link код`.</p>
        </div>

        <div v-if="telegramCode" class="code-box">
          /link {{ telegramCode }}
        </div>

        <button class="button ghost" type="button" @click="makeTelegramCode">
          {{ telegramCode ? 'обновить код' : 'получить код' }}
        </button>
      </section>

      <div class="auth-actions">
        <button class="button ghost" type="button" @click="$emit('close')">закрыть</button>
        <button class="button primary" :disabled="saveDisabled">
          {{ saveText }}
        </button>
      </div>
    </form>
  </Modal>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import Modal from '../../components/ui/Modal.vue'
import { useStore } from '../../store/store.js'
import { fileUrl } from '../../api/users.js'

const emit = defineEmits(['close'])
const { state, checkUsername, loadProfile, updateProfile, uploadAvatar, createTelegramLinkCode } = useStore()

const error = ref('')
const message = ref('')
const usernameMessage = ref('')
const usernameStatus = ref('available')
const saving = ref(false)
const avatar = ref(null)
const previewUrl = ref('')
const telegramCode = ref('')

const form = reactive({
  email: '',
  username: '',
  name: '',
  photo_url: '',
  tg_id: null,
})

const avatarLetter = computed(() => (form.name || form.username || '?').slice(0, 1).toUpperCase())
const usernameReady = computed(() => form.username === state.auth.user?.username || usernameStatus.value === 'available')
const saveDisabled = computed(() => saving.value || !usernameReady.value)
const saveText = computed(() => {
  if (saving.value) return 'сохраняем...'
  if (usernameStatus.value === 'checking') return 'проверяем...'
  return 'сохранить'
})

onMounted(async () => {
  const user = await loadProfile().catch(() => null)
  fill(user || state.auth.user)
})

function fill(user) {
  form.email = user?.email || ''
  form.username = user?.username || ''
  form.name = user?.name || ''
  form.photo_url = user?.photo_url || ''
  form.tg_id = user?.tg_id || null
  previewUrl.value = user?.photoUrl || fileUrl(user?.photo_url) || ''
  usernameStatus.value = 'available'
}

watch(
  () => form.username,
  (username) => {
    usernameMessage.value = ''
    if (username === state.auth.user?.username) {
      usernameStatus.value = 'available'
      return
    }

    usernameStatus.value = 'idle'
  }
)

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
    fail('Выберите картинку png, jpg или webp.')
    return
  }

  avatar.value = await resizeAvatar(file)
  if (previewUrl.value?.startsWith('blob:')) URL.revokeObjectURL(previewUrl.value)
  previewUrl.value = URL.createObjectURL(avatar.value)
  error.value = ''
}

async function checkName() {
  usernameMessage.value = ''
  if (form.username === state.auth.user?.username) {
    usernameStatus.value = 'available'
    return
  }

  if (!form.username || form.username.length < 3) {
    usernameStatus.value = 'idle'
    return
  }

  try {
    usernameStatus.value = 'checking'
    const available = await checkUsername(form.username)
    usernameStatus.value = available ? 'available' : 'taken'
    usernameMessage.value = available ? 'Username доступен.' : ''
    if (!available) fail('Username уже занят.')
  } catch {
    usernameStatus.value = 'idle'
    fail(state.error)
  }
}

async function save() {
  error.value = ''
  message.value = ''
  usernameMessage.value = ''

  if (form.username.length < 3) {
    fail('Username должен быть не короче 3 символов.')
    return
  }

  if (!usernameReady.value) {
    fail('Сначала проверьте доступность username.')
    return
  }

  saving.value = true

  try {
    const photoUrl = avatar.value ? await uploadAvatar(avatar.value) : form.photo_url
    const user = await updateProfile({ ...form, photo_url: photoUrl })
    fill(user)
    avatar.value = null
    message.value = 'Профиль сохранен.'
  } catch {
    fail(state.error)
  } finally {
    saving.value = false
  }
}

async function makeTelegramCode() {
  error.value = ''
  message.value = ''

  try {
    telegramCode.value = await createTelegramLinkCode()
  } catch {
    fail(state.error)
  }
}
</script>
