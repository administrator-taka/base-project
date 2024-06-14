<template>
  <div>
    <main class="main-content">
      <h1>動画ホーム画面</h1>
      <!-- <img
        v-if="videoData && videoData.thumbnail"
        :src="
        'https://img.youtube.com/vi/' +
        videoData.videoId +
        '/maxresdefault.jpg'
        "
        alt="Image"
        /> -->
      <div v-if="videoData && videoData.videoId">
        <div class="col-md-3">
          <button
            @click="goToChannelPage(videoData.channelId)"
            class="btn btn-secondary m-2"
          >
            <i class="bi bi-arrow-90deg-down"></i>
            チャンネルページへ
          </button>
        </div>
        <div class="ratio ratio-16x9">
          <iframe
            loading="lazy"
            :src="'https://www.youtube.com/embed/' + videoData.videoId"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          ></iframe>
        </div>
        <a :href="'https://youtu.be/' + videoData.videoId" target="_blank">
          {{ 'https://youtu.be/' + videoData.videoId }}
        </a>
        <div class="col-md-3">
          <h2>字幕データ更新</h2>
          <button @click="downloadVideoSubtitle" class="btn btn-danger m-2">
            <i class="bi bi-exclamation-triangle"></i> 字幕をダウンロード
          </button>
          <h2>字幕言語指定</h2>
          <DropdownSelect
            :options="languageCode"
            v-model="selectedLanguageCode"
          />
        </div>
      </div>
      <JsonTable v-if="videoData" :data="videoData" />
      <div v-if="subtitleList">
        <h2>字幕一覧</h2>
        <div v-for="(subtitle, index) in subtitleList" :key="index">
          <RangeSelector
            @range-selected="openModal(subtitle.subtitleTextId)"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
          >
            <div class="m-3">
              <!-- TODO:モーダル修正後に削除 -->
              <div style="height: 1rem"></div>
              <JsonTable :data="subtitle" />
            </div>
          </RangeSelector>
        </div>
      </div>
      <SubtitleDetailModal
        :subtitleTextId="selectedSubtitleTextId"
        :languageCode="selectedLanguageCode"
        @update="getVideoData()"
      />
    </main>
  </div>
</template>

<script lang="ts">
import videoRepository from '@/api/repository/video-repository'
import SubtitleDetailModal from '@/components/youtube-app/subtitle/SubtitleDetailModal.vue'
import JsonTable from '@/components/common/table/JsonTable.vue'

import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getYouTubeLanguagesFromCodes } from '@/enums/youtube-language' // ここで関数をインポート
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import RangeSelector from '@/components/common/button/RangeSelector.vue'
import { showErrorToast, showSuccessToast } from '@/utils/toast-service'

export default {
  components: {
    SubtitleDetailModal,
    JsonTable,
    DropdownSelect,
    RangeSelector
  },
  setup() {
    const route = useRoute()
    const videoId = ref<string>(
      typeof route.params.videoId === 'string' ? route.params.videoId : ''
    )
    const videoData = ref()
    const subtitleList = ref()
    const selectedSubtitleTextId = ref<string>('')
    const selectedLanguageCode = ref<string>('')
    const router = useRouter()
    const languageCode = ref([{ name: '', value: '' }])

    const downloadVideoSubtitle = async () => {
      videoRepository
        .downloadVideoSubtitle(videoId.value)
        .then((response) => {
          console.log(response)
          getVideoData()
          showSuccessToast('字幕ダウンロード処理')
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }

    const getVideoData = async () => {
      videoRepository
        .getVideoData(videoId.value)
        .then((response) => {
          videoData.value = response.videoData
          languageCode.value = getYouTubeLanguagesFromCodes(
            response.videoData.translationLanguages
          )
          selectedLanguageCode.value =
            response.videoData.translationLanguages[0]
          console.log(languageCode.value)
          subtitleList.value = response.subtitleList
          console.log(response)
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }

    const openModal = (subtitleTextId: string) => {
      selectedSubtitleTextId.value = subtitleTextId
    }
    const goToChannelPage = (channelId: string) => {
      router.push(`/channel/${channelId}`)
    }
    onMounted(() => {
      getVideoData()
    })
    return {
      videoData,
      subtitleList,
      selectedSubtitleTextId,
      selectedLanguageCode,
      openModal,
      downloadVideoSubtitle,
      goToChannelPage,
      languageCode,
      getVideoData
    }
  }
}
</script>

<style scoped></style>
