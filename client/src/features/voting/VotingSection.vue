<template>
  <section class="panel">
    <header class="section-header">
      <div>
        <p class="eyebrow">Р°РєС‚РёРІРЅРѕРµ РіРѕР»РѕСЃРѕРІР°РЅРёРµ</p>
        <h2>{{ voting ? titleByType[voting.type] : 'Р“РѕР»РѕСЃРѕРІР°РЅРёРµ РЅРµ СЃРѕР·РґР°РЅРѕ' }}</h2>
      </div>

      <div class="topbar-actions">
        <button v-if="!voting" class="button primary" @click="$emit('create', 'yes_no')">
          СЃРѕР·РґР°С‚СЊ
        </button>
        <button v-if="!voting" class="button ghost" @click="$emit('create', 'like')">
          like
        </button>
        <button v-if="voting" class="button ghost" @click="$emit('delete', voting.id)">
          СѓРґР°Р»РёС‚СЊ
        </button>
      </div>
    </header>

    <div v-if="voting && ideas.length" class="vote-list">
      <article v-for="idea in ideas" :key="idea.id" class="vote-card">
        <div class="vote-text">
          <h3>{{ idea.title }}</h3>
          <p>{{ idea.description }}</p>
        </div>

        <div class="vote-actions">
          <button class="button ghost" @click="$emit('open', idea)">РѕС‚РєСЂС‹С‚СЊ</button>
          <button class="button primary" @click="$emit('vote', idea.id)">РіРѕР»РѕСЃ</button>
        </div>
      </article>
    </div>

    <EmptyState
      v-else
      title="РќРµС‚ РёРґРµР№ РґР»СЏ РіРѕР»РѕСЃРѕРІР°РЅРёСЏ"
      text="Р’ РіРѕР»РѕСЃРѕРІР°РЅРёРё СѓС‡Р°СЃС‚РІСѓСЋС‚ С‚РѕР»СЊРєРѕ РѕРґРѕР±СЂРµРЅРЅС‹Рµ РёРґРµРё."
    />

    <section class="results-panel">
      <h3>Р РµР·СѓР»СЊС‚Р°С‚С‹</h3>

      <button v-for="result in results" :key="result.id" class="result-row" @click="$emit('open', result)">
        <span>{{ result.title }}</span>
        <strong>{{ result.votesCount }} / {{ result.approvalPercent }}%</strong>
      </button>
    </section>
  </section>
</template>

<script setup>
import EmptyState from '../../components/ui/EmptyState.vue'

defineProps({
  ideas: { type: Array, default: () => [] },
  results: { type: Array, default: () => [] },
  voting: { type: Object, default: null },
})

defineEmits(['open', 'vote', 'create', 'delete'])

const titleByType = {
  like: 'Like-РіРѕР»РѕСЃРѕРІР°РЅРёРµ',
  yes_no: 'Р“РѕР»РѕСЃРѕРІР°РЅРёРµ',
}
</script>
