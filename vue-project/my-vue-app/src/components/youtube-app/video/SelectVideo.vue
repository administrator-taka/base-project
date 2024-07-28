<template>
  <div>
    <h2>YouTube動画IDとタイムスタンプ抽出器</h2>
    <div class="col-md-6">
      <input
        v-model="youtubeUrl"
        type="text"
        class="form-control"
        placeholder="YouTube動画のURLを入力"
        required
      />
    </div>
    <div v-if="videoId">
      <h3>抽出された動画ID</h3>
      <p>{{ videoId }}</p>
      <button @click="goToVideoPage(videoId)" class="btn btn-primary m-2">
        動画ページへ
      </button>

      <h3 v-if="timestamp !== null">抽出されたタイムスタンプ</h3>
      <p v-if="timestamp !== null">{{ timestamp }} 秒</p>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, watch, defineComponent } from 'vue'
import router from '@/router'

export default defineComponent({
  setup(_, { emit }) {
    const youtubeUrl = ref('')
    const videoId = ref('')
    const timestamp = ref<number | null>(null)

    const extractVideoDetails = () => {
      const url = youtubeUrl.value

      // YouTube動画IDを抽出する正規表現
      const videoIdMatch = url.match(
        /(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/|user\/(?:[^#&?]*).*))([^#&?]*)/
      )
      videoId.value =
        videoIdMatch && videoIdMatch[1].length === 11 ? videoIdMatch[1] : ''

      // タイムスタンプを抽出する正規表現
      const timestampMatch = url.match(/[?&]t=(\d+)/)
      timestamp.value = timestampMatch ? parseInt(timestampMatch[1], 10) : null

      emit('update:videoDetails', {
        videoId: videoId.value,
        timestamp: timestamp.value
      })
    }

    const goToVideoPage = (videoId: string) => {
      router.push(`/video/${videoId}`)
    }

    // youtubeUrlが変更されるたびにextractVideoDetailsを実行
    watch(youtubeUrl, extractVideoDetails)

    return {
      youtubeUrl,
      videoId,
      timestamp,
      goToVideoPage
    }
  }
})
</script>

<style scoped>
/* スタイルを追加 */
</style>
