<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <div>チャンネルホーム画面</div>
      <img
        v-if="channelData && channelData.thumbnail"
        :src="channelData.thumbnail"
        alt="Image"
      />
      <pre>{{ JSON.stringify(channelData, null, 2) }}</pre>
      <div v-if="videoList">
        <h2>動画一覧</h2>
        <ul>
          <li v-for="(video, index) in videoList" :key="index">
            <!-- 字幕データがあるもののみ一旦表示 -->
            <div
              v-if="
                video.infos &&
                video.infos.some(
                  (info) =>
                    info.languageCode === 'ko' && info.subtitleStatus === 1
                ) &&
                video.infos.some(
                  (info) =>
                    info.languageCode === 'ja' && info.subtitleStatus === 1
                )
              "
            >
              <img :src="video.thumbnail" alt="Image" />
              <button @click="goToVideoPage(video)">動画ページへ</button>
              <pre>{{ JSON.stringify(video, null, 2) }}</pre>
            </div>
          </li>
        </ul>
      </div>
    </main>
  </div>
</template>

<script>
import Sidebar from '@/components/SidebarComponent.vue'
import channelRepository from '@/api/repository/channelRepository'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  components: {
    Sidebar
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const channelId = ref(route.params.channelId || '')
    const channelData = ref()
    const videoList = ref()

    const getChannelData = async () => {
      channelRepository
        .getChannelData(channelId.value)
        .then((response) => {
          channelData.value = response.channelData
          videoList.value = response.videoList
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const downloadChannelSubtitles = async () => {
      channelRepository
        .downloadChannelSubtitles(channelId.value)
        .then((response) => console.log(response))
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const searchWord = async () => {
      channelRepository
        .searchWord(channelId.value, 'YOUR_SEARCH_WORD')
        .then((response) => console.log(response))
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const updateTranslationLanguage = async () => {
      channelRepository
        .updateTranslationLanguage(channelId.value, 'ko', ['ja'])
        .then((response) => console.log(response))
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const goToVideoPage = (video) => {
      router.push(`/video/${video.videoId}`)
    }

    onMounted(() => {
      getChannelData()
    })

    return {
      downloadChannelSubtitles,
      searchWord,
      updateTranslationLanguage,
      channelData,
      videoList,
      goToVideoPage
    }
  }
}
</script>

<style scoped></style>
