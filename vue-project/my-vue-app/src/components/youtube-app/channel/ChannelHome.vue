<template>
  <div>
    <main class="main-content">
      <h1>チャンネルホーム画面</h1>
      <div class="row">
        <div class="col-md-3">
          <img
            v-if="channelData && channelData.thumbnail"
            :src="channelData.thumbnail"
            alt="Image"
            class="img-thumbnail m-2"
          />
        </div>
        <div class="col-md-6">
          <h2>言語更新</h2>
          <form @submit.prevent="updateTranslationLanguage">
            <div class="row g-3">
              <div class="col">
                <label for="languageCodeDropdown" class="form-label"
                  >デフォルト言語</label
                >
                <DropdownSelect
                  :options="languageCode"
                  v-model="selectedLanguageCode"
                />
              </div>
              <div class="col">
                <label for="languageCodeDropdown" class="form-label"
                  >学習言語</label
                >
                <DropdownMultiSelect
                  :options="languageCode"
                  v-model="selectedLanguageCodeList"
                />
              </div>
            </div>
            <button type="submit" class="btn btn-danger m-2">
              <i class="bi bi-exclamation-triangle"></i> 言語更新
            </button>
          </form>
        </div>
        <div class="col-md-3">
          <h2>字幕データ更新</h2>
          <button @click="downloadChannelSubtitles" class="btn btn-danger m-2">
            <i class="bi bi-exclamation-triangle"></i> 字幕をダウンロード
          </button>
        </div>
      </div>
      <JsonTable v-if="channelData" :data="channelData" />
      <!-- 検索フォームの追加 -->
      <div class="m-2">
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
            class="btn btn-primary m-2"
            :disabled="!searchWord"
          >
            <i class="bi bi-search"></i> 検索
          </button>
        </form>
      </div>

      <!-- 検索結果の表示 -->
      <div v-if="searchResults" class="m-2">
        <h2>検索結果</h2>
        <div
          v-if="searchResults.length > 0"
          class="overflow-auto"
          style="height: 1000px"
        >
          <div
            v-for="(result, index) in searchResults"
            :key="index"
            class="mb-2"
          >
            <JsonTable :data="result" />
            <button
              @click="goToVideoPage(result.videoId)"
              class="btn btn-info m-2"
            >
              動画詳細
            </button>
            <a :href="result.youtubeUrl" target="_blank" class="btn btn-link">
              <i class="bi bi-youtube"></i> {{ result.youtubeUrl }}
            </a>
          </div>
        </div>
        <div v-else-if="searchResults.length == 0">結果がありません</div>
      </div>

      <!-- 複数処理結果の表示 -->
      <div v-if="searchMultipleResults" class="m-2">
        <h2>複数処理結果</h2>
        <div
          v-if="searchMultipleResults.length > 0"
          class="overflow-auto"
          style="height: 1000px"
        >
          <div
            v-for="(result, index) in searchMultipleResults"
            :key="index"
            class="mb-2"
          >
            <JsonTable :data="result" />
            <button
              @click="goToVideoPage(result.videoId)"
              class="btn btn-info m-2"
            >
              動画詳細
            </button>
            <a :href="result.youtubeUrl" target="_blank" class="btn btn-link">
              <i class="bi bi-youtube"></i> {{ result.youtubeUrl }}
            </a>
          </div>
        </div>
        <div v-else-if="searchMultipleResults.length == 0">
          結果がありません
        </div>
      </div>
      <div class="m-2">
        <h2>頻出単語集計</h2>
        <form @submit.prevent="calculateChannelWord">
          <div class="row g-3">
            <div class="col-md-3">
              <label for="minWordInput" class="form-label">最小単語数</label>
              <input
                v-model.number="minWord"
                type="number"
                class="form-control m-2"
                id="minWordInput"
                placeholder="最小単語数"
                required
              />
            </div>
            <div class="col-md-3">
              <label for="minWordLengthInput" class="form-label"
                >最小単語の長さ</label
              >
              <input
                v-model.number="minWordLength"
                type="number"
                class="form-control m-2"
                id="minWordLengthInput"
                placeholder="最小単語の長さ"
                required
              />
            </div>
            <div class="col-md-3">
              <label for="topNInput" class="form-label">上位N件</label>
              <input
                v-model.number="topN"
                type="number"
                class="form-control m-2"
                id="topNInput"
                placeholder="上位N件"
                required
              />
            </div>
            <div class="col-md-3">
              <label for="subtitleTypeCodeDropdown" class="form-label"
                >字幕種類</label
              >
              <DropdownSelect
                :options="subtitleTypeCode"
                v-model="subtitleType"
              />
            </div>
          </div>
          <button type="submit" class="btn btn-primary m-2">
            <i class="bi bi-calculator"></i> 計算
          </button>
        </form>

        <div v-if="calculateWord" class="m-2">
          <h2>集計結果</h2>
          <ChartComp
            :chartId="chartId"
            :chartData="chartData"
            :chartOptions="chartOptions"
          />

          <div
            v-if="calculateWord.length > 0"
            class="overflow-auto"
            style="height: 1000px"
          >
            <div
              v-for="(word, index) in calculateWord"
              :key="index"
              class="m-2"
            >
              <div class="row">
                <div class="col-md-8">
                  <div class="m-3">
                    <JsonTable :data="word" />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else-if="calculateWord.length == 0">結果がありません</div>
        </div>
      </div>

      <h2>絞り込み</h2>
      <DropdownMultiSelect
        :options="languageCode"
        v-model="subtitleListLanguages"
      />
      <PaginationComponent
        :currentPage="channelStore.page"
        :totalPages="totalPages"
        @page-changed="handlePageChange"
      />

      <div v-if="videoList">
        <h2>動画一覧(全{{ total }}件)</h2>
        <div class="overflow-auto" style="height: 1000px">
          <div v-for="(video, index) in videoList" :key="index" class="m-2">
            <RangeSelector @range-selected="goToVideoPage(video.videoId)">
              <div class="row">
                <div class="col-md-4">
                  <img
                    :src="video.thumbnail"
                    alt="Image"
                    class="img-thumbnail m-3"
                  />
                </div>
                <div class="col-md-8">
                  <div class="m-3">
                    <JsonTable :data="video" />
                  </div>
                </div>
              </div>
            </RangeSelector>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import channelRepository from '@/api/repository/channelRepository'
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PaginationComponent from '@/components/common/pagination/PaginationComponent.vue'
import DropdownMultiSelect from '@/components/common/dropdown/DropdownMultiSelect.vue'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import { YouTubeLanguageLabel } from '@/enums/youtube-language'
import JsonTable from '@/components/common/table/JsonTable.vue'
import RangeSelector from '@/components/common/button/RangeSelector.vue'
import { useChannelStore } from '@/store/useChannelStore'
import { SubtitleType, SubtitleTypeLabel } from '@/enums/subtitle-type'
import ChartComp from '@/components/common/graph/ChartComp.vue'

interface ChannelWord {
  word: string
  count: number
}
export default {
  components: {
    PaginationComponent,
    DropdownMultiSelect,
    DropdownSelect,
    JsonTable,
    RangeSelector,
    ChartComp
  },
  setup() {
    const channelStore = useChannelStore()

    const route = useRoute()
    const router = useRouter()
    channelStore.channelId =
      typeof route.params.channelId === 'string' ? route.params.channelId : ''

    const channelData = ref()
    const videoList = ref()

    const searchWord = ref('')
    const searchResults = ref()
    const searchMultipleResults = ref()

    const getChannelData = async () => {
      channelRepository
        .getChannelData(channelStore.channelId)
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

    const minWord = ref(1)
    const minWordLength = ref(2)
    const topN = ref(100)
    const subtitleTypeCode = SubtitleTypeLabel
    const subtitleType = ref<number>(SubtitleType.MANUAL)
    const calculateWord = ref()
    const chartId = 'my-chart-id'
    const chartData = ref({
      labels: [] as string[],
      datasets: [
        {
          label: '頻出単語集計',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
          data: [] as number[]
        }
      ]
    })
    const chartOptions = {
      responsive: true
    }

    const calculateChannelWord = async () => {
      channelRepository
        .calculateChannelWord(
          channelStore.channelId,
          minWord.value,
          minWordLength.value,
          topN.value,
          subtitleType.value
        )
        .then((response) => {
          calculateWord.value = response.calculateWord
          console.log(response)
          const data = response.calculateWord as ChannelWord[]

          chartData.value.labels = data.map((item) => item.word)
          chartData.value.datasets[0].data = data.map((item) => item.count)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }
    const totalPages = ref(1)
    const total = ref(0)
    const getChannelVideoList = async () => {
      channelRepository
        .getChannelVideoList(
          channelStore.channelId,
          channelStore.page,
          channelStore.pageSize,
          channelStore.languages
        )
        .then((response) => {
          console.log(response)
          totalPages.value = parseInt(
            response.results.paginationInfo.totalPages
          )
          channelStore.page = parseInt(response.results.paginationInfo.page)
          total.value = parseInt(response.results.paginationInfo.total)
          videoList.value = response.results.videoList
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const handlePageChange = (page: number) => {
      channelStore.page = page
      getChannelVideoList()
    }

    const search = async () => {
      channelRepository
        .searchWord(channelStore.channelId, searchWord.value)
        .then((response) => {
          searchResults.value = response.searchResults
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
      channelRepository
        .searchMultipleWord(channelStore.channelId, searchWord.value)
        .then((response) => {
          searchMultipleResults.value = response.searchMultipleResults
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const downloadChannelSubtitles = async () => {
      channelRepository
        .downloadChannelSubtitles(channelStore.channelId)
        .then((response) => {
          console.log(response)
          getChannelData()
          getChannelVideoList()
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const updateTranslationLanguage = async () => {
      channelRepository
        .updateTranslationLanguage(
          channelStore.channelId,
          selectedLanguageCode.value,
          selectedLanguageCodeList.value
        )
        .then((response) => {
          console.log(response)
          getChannelData()
          getChannelVideoList()
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
    const subtitleListLanguages = ref(channelStore.languages)
    watch(subtitleListLanguages, () => {
      channelStore.languages = subtitleListLanguages.value
      channelStore.setPage(1) // ページをリセット
      channelStore.setPageSize(10) // ページサイズをリセット
      getChannelVideoList()
    })

    return {
      channelData,
      videoList,
      goToVideoPage,
      search,
      searchResults,
      searchMultipleResults,
      searchWord,
      downloadChannelSubtitles,
      totalPages,
      handlePageChange,
      updateTranslationLanguage,
      total,
      languageCode,
      selectedLanguageCodeList,
      selectedLanguageCode,
      channelStore,
      subtitleListLanguages,
      calculateChannelWord,
      minWord,
      minWordLength,
      topN,
      subtitleTypeCode,
      subtitleType,
      calculateWord,
      chartId,
      chartData,
      chartOptions
    }
  }
}
</script>

<style scoped></style>
