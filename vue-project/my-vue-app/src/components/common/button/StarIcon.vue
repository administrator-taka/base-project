<template>
  <div>
    <div class="star-icon" @click="toggleFavorite">
      <!-- favoriteプロパティに応じて星アイコンを切り替える -->
      <i v-if="modelValue" class="bi bi-star-fill"></i>
      <i v-else class="bi bi-star"></i>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  setup(props, { emit }) {
    const toggleFavorite = () => {
      emit('update:modelValue', !props.modelValue)
      emit('update') // 更新イベントを発火する
    }

    return {
      toggleFavorite
    }
  }
})
</script>

<style scoped>
.star-icon {
  cursor: pointer; /* カーソルをポインターに変更してクリック可能であることを示す */
  display: inline-block; /* ボタンサイズをアイコンに合わせるためにインラインブロック要素とする */
}
.star-icon i {
  font-size: 1.5rem; /* アイコンのサイズを適宜調整 */
}
</style>
