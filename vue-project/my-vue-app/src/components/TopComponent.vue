<template>
  <div>
    <main class="main-content">
      <div>トップ画面（仮）</div>
      <SelectVideo></SelectVideo>
    </main>
  </div>
</template>

<script lang="ts">
import SelectVideo from './youtube-app/video/SelectVideo.vue'

export default {
  components: { SelectVideo }
}
</script>

<style scoped></style>
