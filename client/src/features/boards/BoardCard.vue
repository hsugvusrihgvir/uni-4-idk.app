<template>
  <article class="board-card" @click="$emit('open', board.id)">
    <div class="board-decor">✦</div>

    <header class="board-card-header">
      <span class="chip">{{ board.role }}</span>

      <button v-if="board.role === 'admin'" class="text-danger mini-delete" type="button" @click.stop="$emit('remove', board.id)">
        удалить
      </button>
    </header>

    <div class="board-content">
      <h2>{{ board.title }}</h2>
      <p>{{ board.description || 'Описание доски' }}</p>
    </div>

    <footer class="board-stats">
      <div>
        <strong>{{ ideasCount }}</strong>
        <span>идей</span>
      </div>

      <div>
        <strong>{{ board.membersCount ?? board.members?.length ?? 0 }}</strong>
        <span>участников</span>
      </div>
    </footer>
  </article>
</template>

<script setup>
defineProps({
  board: { type: Object, required: true },
  ideasCount: { type: Number, default: 0 },
})

defineEmits(['open', 'remove'])
</script>
