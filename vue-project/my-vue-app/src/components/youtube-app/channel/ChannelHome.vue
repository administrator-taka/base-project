<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <h1>チャンネルホーム画面</h1>
      <img
        v-if="channelData && channelData.thumbnail"
        :src="channelData.thumbnail"
        alt="Image"
        style="width: 200px"
      />
      <pre>{{ JSON.stringify(channelData, null, 2) }}</pre>
      <div class="col-md-3">
        <label for="languageCodeDropdown" class="form-label"
          >デフォルト言語</label
        >
        <DropdownSelect
          :options="languageCode"
          v-model="selectedLanguageCode"
        />
      </div>
      <div class="col-md-3">
        <label for="languageCodeDropdown" class="form-label">学習言語</label>
        <DropdownMultiSelect
          :options="languageCode"
          v-model="selectedLanguageCodeList"
        />
      </div>

      <button @click="updateTranslationLanguage" class="btn btn-success ms-2">
        言語更新
      </button>
      <!-- 検索フォームの追加 -->
      <div class="mb-3">
        <form @submit.prevent="search">
          <h2>出現箇所検索</h2>
          <div class="col-md-6">
            <input
              v-model="searchWord"
              type="text"
              class="form-control"
              placeholder="検索ワードを入力"
              required
            />
          </div>
          <button
            type="submit"
            class="btn btn-primary mt-2"
            :disabled="!searchWord"
          >
            検索
          </button>
        </form>
      </div>

      <!-- 検索結果の表示 -->
      <div v-if="searchResults" class="mb-3">
        <h2>検索結果</h2>
        <div v-for="(result, index) in searchResults" :key="index" class="mb-2">
          <pre>{{ JSON.stringify(result, null, 2) }}</pre>
          <button
            @click="goToVideoPage(result.videoId)"
            class="btn btn-info mt-2"
          >
            動画ページへ
          </button>
          <a :href="result.youtubeUrl" target="_blank" class="btn btn-link">
            {{ result.youtubeUrl }}
          </a>
        </div>
      </div>

      <div class="mb-3">
        <button @click="downloadChannelSubtitles" class="btn btn-danger ms-2">
          字幕をダウンロード
        </button>
      </div>
      <PaginationComponent
        :currentPage="currentPage"
        :totalPages="totalPages"
        @page-changed="handlePageChange"
      />

      <div v-if="videoList">
        <h2>動画一覧(全{{ total }}件)</h2>
        <button @click="toggleSubtitleFilter" class="btn btn-secondary ms-2">
          字幕フィルターを切り替える
        </button>
        <div v-for="(video, index) in videoList" :key="index" class="mb-3">
          <div v-if="shouldDisplayVideo(video)">
            <img :src="video.thumbnail" alt="Image" class="img-thumbnail" />
            <button
              @click="goToVideoPage(video.videoId)"
              class="btn btn-info mt-2"
            >
              動画ページへ
            </button>
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
import PaginationComponent from '@/components/common/pagination/PaginationComponent.vue'
import DropdownMultiSelect from '@/components/common/dropdown/DropdownMultiSelect.vue'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import { YouTubeLanguageLabel } from '@/enums/youtube-language'

export default {
  components: {
    Sidebar,
    PaginationComponent,
    DropdownMultiSelect,
    DropdownSelect
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
          selectedLanguageCode.value = response.channelData.defaultAudioLanguage
          selectedLanguageCodeList.value =
            response.channelData.translationLanguages
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const currentPage = ref(1)
    const totalPages = ref(1)
    const pageSize = 30 // 1ページあたりのアイテム数
    const total = ref(0)
    const getChannelVideoList = async () => {
      channelRepository
        .getChannelVideoList(channelId.value, currentPage.value, pageSize)
        .then((response) => {
          console.log(response)
          totalPages.value = parseInt(
            response.results.paginationInfo.totalPages
          )
          currentPage.value = parseInt(response.results.paginationInfo.page)
          total.value = parseInt(response.results.paginationInfo.total)
          videoList.value = response.results.videoList
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const handlePageChange = (page: number) => {
      currentPage.value = page
      getChannelVideoList()
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

    const downloadChannelSubtitles = async () => {
      channelRepository
        .downloadChannelSubtitles(channelId.value)
        .then((response) => {
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

    const updateTranslationLanguage = async () => {
      channelRepository
        .updateTranslationLanguage(
          channelId.value,
          selectedLanguageCode.value,
          selectedLanguageCodeList.value
        )
        .then((response) => {
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const goToVideoPage = (videoId: string) => {
      router.push(`/video/${videoId}`)
    }
    const languageCode = YouTubeLanguageLabel
    const selectedLanguageCode = ref()
    const selectedLanguageCodeList = ref([])

    onMounted(() => {
      getChannelData()
      getChannelVideoList()
    })

    return {
      toggleSubtitleFilter,
      channelData,
      videoList,
      goToVideoPage,
      shouldDisplayVideo,
      search,
      searchResults,
      searchWord,
      downloadChannelSubtitles,
      currentPage,
      totalPages,
      handlePageChange,
      updateTranslationLanguage,
      total,
      languageCode,
      selectedLanguageCodeList,
      selectedLanguageCode
    }
  }
}
</script>

<style scoped></style>
