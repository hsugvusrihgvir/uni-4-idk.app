<template>
  <article class="idea-card" @click="$emit('open', idea)">
    <div class="idea-header">
      <h3>{{ idea.title }}</h3>
      <span class="idea-mark"></span>
    </div>

    <div class="idea-main">
      <p>{{ idea.description }}</p>
    </div>

    <div class="idea-meta">
      <span>{{ idea.createdAt || idea.date }}</span>
      <button
        v-if="!idea.isAnonymous"
        class="author-link"
        type="button"
        @click.stop="$emit('open-author', idea)"
      >
        {{ idea.author }}
      </button>
      <span v-else>{{ labels.anonymous }}</span>
    </div>

    <div class="idea-footer">
      <button v-if="canDelete" class="text-danger" @click.stop="$emit('remove', idea.id)">
        {{ labels.delete }}
      </button>
    </div>
  </article>
</template>

<script setup>
defineProps({
  idea: { type: Object, required: true },
  canDelete: { type: Boolean, default: true },
})

defineEmits(['open', 'remove', 'open-author'])

const labels = {
  anonymous: '\u0430\u043d\u043e\u043d\u0438\u043c\u043d\u043e',
  delete: '\u0443\u0434\u0430\u043b\u0438\u0442\u044c',
}
</script>
