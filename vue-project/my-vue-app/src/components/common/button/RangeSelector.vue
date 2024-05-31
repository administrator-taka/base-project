<template>
  <div @click="handleRangeClick" class="hoverable">
    <slot></slot>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue'

const emit = defineEmits(['range-selected'])

const handleRangeClick = () => {
  // 範囲の処理を行う（例：親コンポーネントにイベントを発火するなど）
  emit('range-selected')
}
</script>

<style scoped>
.hoverable:hover {
  /* ホバー時のスタイルをここに指定 */
  background-color: rgb(188, 216, 209);
  cursor: pointer;
}
</style>
