<template>
  <Modal title="Экспорт идей" label="html" @close="$emit('close')">
    <div class="modal-form">
      <label class="field">
        Минимальный процент одобрения
        <input v-model.number="threshold" type="number" min="0" max="100" />
      </label>

      <section class="export-summary">
        <div>
          <strong>{{ exportedIdeas.length }}</strong>
          <span>идей попадет в файл</span>
        </div>
        <div>
          <strong>{{ threshold }}%</strong>
          <span>минимум одобрения</span>
        </div>
      </section>

      <button class="button primary" @click="download">скачать html-отчет</button>
    </div>
  </Modal>
</template>

<script setup>
import { computed, ref } from 'vue'
import Modal from '../../components/ui/Modal.vue'

const props = defineProps({
  ideas: { type: Array, default: () => [] },
  board: { type: Object, default: () => ({}) },
})

defineEmits(['close'])

const threshold = ref(50)
const exportedIdeas = computed(() =>
  props.ideas
    .filter((idea) => Number(idea.approvalPercent || 0) >= threshold.value)
    .sort((a, b) => Number(b.approvalPercent || 0) - Number(a.approvalPercent || 0))
)

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

function formatDate(value = new Date()) {
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  }).format(new Date(value))
}

function fileName(value) {
  return String(value || 'ideas')
    .toLowerCase()
    .replace(/[^a-zа-яё0-9]+/gi, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 42) || 'ideas'
}

function ideaCard(idea, index) {
  const title = escapeHtml(idea.title || `Идея ${index + 1}`)
  const description = escapeHtml(idea.description || 'Без описания')
  const votes = Number(idea.votesCount ?? idea.votesYes ?? 0)
  const approval = Number(idea.approvalPercent || 0)

  return `
    <article class="idea-card">
      <header>
        <span class="number">${String(index + 1).padStart(2, '0')}</span>
        <div>
          <h2>${title}</h2>
          <p>${description}</p>
        </div>
      </header>
      <footer>
        <span>${votes} голосов</span>
        <strong>${approval}% одобрения</strong>
      </footer>
      <div class="bar"><span style="width: ${Math.max(0, Math.min(approval, 100))}%"></span></div>
    </article>
  `
}

function buildHtml() {
  const title = escapeHtml(props.board?.title || 'Идеи')
  const description = escapeHtml(props.board?.description || 'Экспорт идей из idk.app')
  const date = formatDate()
  const ideas = exportedIdeas.value

  return `<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${title} — идеи</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: #3f343a;
      background: #fff7f1;
      font: 16px/1.55 Inter, "Segoe UI", Arial, sans-serif;
    }
    .page {
      max-width: 960px;
      margin: 0 auto;
      padding: 48px 28px;
    }
    .hero {
      border: 1px solid rgba(143, 92, 110, .18);
      border-radius: 28px;
      padding: 34px;
      background:
        radial-gradient(circle at 88% 22%, rgba(237, 141, 173, .28), transparent 26%),
        linear-gradient(135deg, rgba(255,255,255,.92), rgba(255,236,226,.74));
      box-shadow: 0 18px 52px rgba(120, 72, 88, .12);
    }
    .eyebrow {
      margin: 0 0 8px;
      color: #b84f78;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    h1 {
      margin: 0;
      color: #463942;
      font-size: clamp(34px, 7vw, 62px);
      line-height: .95;
      letter-spacing: -.02em;
    }
    .hero-text {
      max-width: 680px;
      margin: 18px 0 0;
      color: #7c6671;
    }
    .meta {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin: 22px 0 0;
    }
    .meta div,
    .empty {
      border: 1px solid rgba(143, 92, 110, .14);
      border-radius: 18px;
      padding: 14px 16px;
      background: rgba(255,255,255,.68);
    }
    .meta strong {
      display: block;
      color: #463942;
      font-size: 22px;
      line-height: 1.1;
    }
    .meta span {
      color: #8a717b;
      font-size: 13px;
      font-weight: 700;
    }
    .ideas {
      display: grid;
      gap: 16px;
      margin-top: 24px;
    }
    .idea-card {
      break-inside: avoid;
      border: 1px solid rgba(143, 92, 110, .16);
      border-radius: 24px;
      padding: 22px;
      background: rgba(255,255,255,.84);
      box-shadow: 0 10px 30px rgba(120, 72, 88, .08);
    }
    .idea-card header {
      display: grid;
      grid-template-columns: 54px minmax(0, 1fr);
      gap: 16px;
    }
    .number {
      width: 46px;
      height: 46px;
      display: grid;
      place-items: center;
      border-radius: 16px;
      color: #b84f78;
      background: #fff0f4;
      font-weight: 900;
    }
    h2 {
      margin: 0 0 8px;
      color: #463942;
      font-size: 24px;
      line-height: 1.15;
    }
    .idea-card p {
      margin: 0;
      color: #6f5a64;
      white-space: pre-wrap;
    }
    .idea-card footer {
      display: flex;
      justify-content: space-between;
      gap: 14px;
      margin-top: 18px;
      color: #8a717b;
      font-size: 14px;
      font-weight: 800;
    }
    .idea-card footer strong {
      color: #b84f78;
    }
    .bar {
      height: 8px;
      margin-top: 12px;
      overflow: hidden;
      border-radius: 999px;
      background: #f3dfe5;
    }
    .bar span {
      display: block;
      height: 100%;
      border-radius: inherit;
      background: linear-gradient(90deg, #d86f96, #eba76f);
    }
    .empty {
      margin-top: 24px;
      color: #7c6671;
      text-align: center;
    }
    @media print {
      body { background: #fff; }
      .page { max-width: none; padding: 0; }
      .hero, .idea-card { box-shadow: none; }
    }
    @media (max-width: 680px) {
      .page { padding: 22px 14px; }
      .hero { padding: 24px; }
      .meta { grid-template-columns: 1fr; }
      .idea-card header { grid-template-columns: 1fr; }
      .idea-card footer { flex-direction: column; }
    }
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <p class="eyebrow">idk.app · экспорт идей</p>
      <h1>${title}</h1>
      <p class="hero-text">${description}</p>
      <section class="meta">
        <div><strong>${ideas.length}</strong><span>идей в отчете</span></div>
        <div><strong>${threshold.value}%</strong><span>порог одобрения</span></div>
        <div><strong>${date}</strong><span>дата экспорта</span></div>
      </section>
    </section>

    ${
      ideas.length
        ? `<section class="ideas">${ideas.map(ideaCard).join('')}</section>`
        : '<section class="empty">Нет идей, подходящих под выбранный порог одобрения.</section>'
    }
  </main>
</body>
</html>`
}

function download() {
  const blob = new Blob([buildHtml()], { type: 'text/html;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${fileName(props.board?.title)}-ideas.html`
  link.click()
  URL.revokeObjectURL(url)
}
</script>
