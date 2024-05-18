<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <h1>チャンネルホーム画面</h1>
      <img
        v-if="channelData && channelData.thumbnail"
        :src="channelData.thumbnail"
        alt="Image"
      />
      <pre>{{ JSON.stringify(channelData, null, 2) }}</pre>

      <!-- 検索フォームの追加 -->
      <div>
        <input
          v-model="searchWord"
          type="text"
          placeholder="検索ワードを入力"
        />
        <button @click="search()">検索</button>
      </div>

      <!-- 検索結果の表示 -->
      <div v-if="searchResults">
        <h2>検索結果</h2>
        <div v-for="(result, index) in searchResults" :key="index">
          <pre>{{ JSON.stringify(result, null, 2) }}</pre>
          <a :href="result.youtubeUrl" target="_blank">
            {{ result.youtubeUrl }}
          </a>
        </div>
      </div>

      <button @click="toggleSubtitleFilter">字幕フィルターを切り替える</button>
      <div v-if="videoList">
        <h2>動画一覧</h2>
        <div v-for="(video, index) in videoList" :key="index">
          <div v-if="shouldDisplayVideo(video)">
            <img :src="video.thumbnail" alt="Image" />
            <button @click="goToVideoPage(video.videoId)">動画ページへ</button>
            <pre>{{ JSON.stringify(video, null, 2) }}</pre>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
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
    const channelId = ref<string>(
      typeof route.params.channelId === 'string' ? route.params.channelId : ''
    )

    const channelData = ref()
    const videoList = ref()
    const showSubtitles = ref(true) // 初期値はtrue

    const searchWord = ref('')
    const searchResults = ref()

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

    const search = async () => {
      channelRepository
        .searchWord(channelId.value, searchWord.value)
        .then((response) => {
          searchResults.value = response.searchResults
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    // ボタン押下で字幕フィルターの状態を切り替える関数
    const toggleSubtitleFilter = () => {
      showSubtitles.value = !showSubtitles.value
    }

    // videoが表示されるべきかどうかを判定する関数
    const shouldDisplayVideo = (video: {
      infos: { languageCode: string; subtitleStatus: number }[]
    }) => {
      if (!video.infos) return false

      // 字幕フィルターが有効の場合
      if (showSubtitles.value) {
        return (
          video.infos.some(
            (info: { languageCode: string; subtitleStatus: number }) =>
              info.languageCode === 'ko' && info.subtitleStatus === 1
          ) &&
          video.infos.some(
            (info: { languageCode: string; subtitleStatus: number }) =>
              info.languageCode === 'ja' && info.subtitleStatus === 1
          )
        )
      } else {
        // 字幕フィルターが無効の場合は常にtrueを返す
        return true
      }
    }

    const goToVideoPage = (videoId: string) => {
      router.push(`/video/${videoId}`)
    }

    onMounted(() => {
      getChannelData()
    })

    return {
      toggleSubtitleFilter,
      channelData,
      videoList,
      goToVideoPage,
      shouldDisplayVideo,
      search,
      searchResults,
      searchWord
    }
  }
}
</script>

<style scoped></style>
