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
      <SearchWord></SearchWord>
      <CaluculateWord></CaluculateWord>

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
import channelRepository from '@/api/repository/channel-repository'
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PaginationComponent from '@/components/common/pagination/PaginationComponent.vue'
import DropdownMultiSelect from '@/components/common/dropdown/DropdownMultiSelect.vue'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import { YouTubeLanguageLabel } from '@/enums/youtube-language'
import JsonTable from '@/components/common/table/JsonTable.vue'
import RangeSelector from '@/components/common/button/RangeSelector.vue'
import { useChannelStore } from '@/store/use-channel-store'
import CaluculateWord from '@/components/youtube-app/channel/CalculateWord.vue'
import SearchWord from '@/components/youtube-app/channel/SearchWord.vue'

export default {
  components: {
    PaginationComponent,
    DropdownMultiSelect,
    DropdownSelect,
    JsonTable,
    RangeSelector,
    CaluculateWord,
    SearchWord
  },
  setup() {
    const channelStore = useChannelStore()

    const route = useRoute()
    const router = useRouter()
    channelStore.channelId =
      typeof route.params.channelId === 'string' ? route.params.channelId : ''

    const channelData = ref()
    const videoList = ref()

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
      downloadChannelSubtitles,
      totalPages,
      handlePageChange,
      updateTranslationLanguage,
      total,
      languageCode,
      selectedLanguageCodeList,
      selectedLanguageCode,
      channelStore,
      subtitleListLanguages
    }
  }
}
</script>

<style scoped></style>
