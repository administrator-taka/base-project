<template>
  <div @click="handleRangeClick" class="hoverable">
    <slot></slot>
  </div>
</template>

<script setup>
import { defineEmits, onMounted } from 'vue'
import { hexToRgba } from '@/utils/util-color' // 関数をインポート

const emit = defineEmits(['range-selected'])

const handleRangeClick = () => {
  // 範囲の処理を行う（例：親コンポーネントにイベントを発火するなど）
  emit('range-selected')
}

onMounted(() => {
  const hoverBackgroundColorHex = '#BCD8D1'
  const hoverBackgroundColorRgba = hexToRgba(hoverBackgroundColorHex, 1)
  document.documentElement.style.setProperty(
    '--hover-background-color',
    hoverBackgroundColorRgba
  )
})
</script>

<style scoped>
.hoverable:hover {
  /* ホバー時のスタイルをここに指定 */
  background-color: var(--hover-background-color);
  cursor: pointer;
}
</style>
