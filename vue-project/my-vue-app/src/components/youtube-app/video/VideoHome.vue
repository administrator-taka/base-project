<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <h1>動画ホーム画面</h1>
      <img
        v-if="videoData && videoData.thumbnail"
        :src="videoData.thumbnail"
        alt="Image"
      />
      <pre>{{ JSON.stringify(videoData, null, 2) }}</pre>
      <div v-if="videoData && videoData.videoId">
        <a :href="'https://youtu.be/' + videoData.videoId" target="_blank">
          {{ 'https://youtu.be/' + videoData.videoId }}
        </a>
      </div>
      <div v-if="subtitleList">
        <h2>字幕一覧</h2>
        <div v-for="(subtitle, index) in subtitleList" :key="index">
          <pre>{{ JSON.stringify(subtitle, null, 2) }}</pre>
        </div>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import Sidebar from '@/components/SidebarComponent.vue'
import videoRepository from '@/api/repository/videoRepository'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

export default {
  components: {
    Sidebar
  },
  setup() {
    const route = useRoute()
    const videoId = ref<string>(
      typeof route.params.videoId === 'string' ? route.params.videoId : ''
    )
    const videoData = ref()
    const subtitleList = ref()

    const getVideoData = async () => {
      videoRepository
        .getVideoData(videoId.value)
        .then((response) => {
          videoData.value = response.videoData
          subtitleList.value = response.subtitleList
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }
    onMounted(() => {
      getVideoData()
    })
    return { videoData, subtitleList }
  }
}
</script>

<style scoped></style>
