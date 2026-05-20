<template>
  <article class="idea-card" @click="$emit('open', idea)">
    <div class="idea-header">
      <h3>{{ idea.title }}</h3>
      <span class="idea-score">вњ¦</span>
    </div>

    <div class="idea-main">
      <p>{{ idea.description }}</p>
    </div>

    <div class="idea-meta">
      <span>{{ idea.createdAt || idea.date }}</span>
      <span>{{ idea.isAnonymous ? 'Р°РЅРѕРЅРёРјРЅРѕ' : idea.author }}</span>
    </div>

    <div class="idea-footer">
      <button v-if="canDelete" class="text-danger" @click.stop="$emit('remove', idea.id)">СѓРґР°Р»РёС‚СЊ</button>
    </div>
  </article>
</template>

<script setup>
defineProps({
  idea: { type: Object, required: true },
  canDelete: { type: Boolean, default: true },
})

defineEmits(['open', 'remove'])
</script>
