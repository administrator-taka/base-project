<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <div>動画ホーム画面</div>
      <img
        v-if="videoData && videoData.thumbnail"
        :src="videoData.thumbnail"
        alt="Image"
      />
      <pre>{{ JSON.stringify(videoData, null, 2) }}</pre>
      <div v-if="subtitleList">
        <h2>字幕一覧</h2>
        <ul>
          <li v-for="(subtitle, index) in subtitleList" :key="index">
            <pre>{{ JSON.stringify(subtitle, null, 2) }}</pre>
          </li>
        </ul>
      </div>
    </main>
  </div>
</template>

<script>
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
    const videoId = ref(route.params.videoId || '')
    const videoData = ref()
    const subtitleList = ref()

    const getVideoData = async () => {
      console.log(videoId.value)
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
