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
        <div>
          <iframe
            loading="lazy"
            width="800"
            height="450"
            :src="'https://www.youtube.com/embed/' + videoData.videoId"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            :allowfullscreen="true"
          ></iframe>
        </div>
        <a :href="'https://youtu.be/' + videoData.videoId" target="_blank">
          {{ 'https://youtu.be/' + videoData.videoId }}
        </a>
      </div>
      <pre>{{ JSON.stringify(videoData, null, 2) }}</pre>
      <div v-if="subtitleList">
        <h2>字幕一覧</h2>
        <div v-for="(subtitle, index) in subtitleList" :key="index">
          <pre>{{ JSON.stringify(subtitle, null, 2) }}</pre>
          <div
            v-for="(subtitleText, index) in subtitle.translations"
            :key="index"
          >
            <button
              type="button"
              class="btn btn-primary"
              @click="
                openModal(subtitle.subtitleTextId, subtitleText.languageCode)
              "
              data-bs-toggle="modal"
              data-bs-target="#exampleModal"
            >
              字幕詳細
            </button>
          </div>
        </div>
      </div>
      <SubtitleDetailModal
        :subtitleTextId="selectedSubtitleTextId"
        :languageCode="selectedLanguageCode"
      />
    </main>
  </div>
</template>

<script lang="ts">
import videoRepository from '@/api/repository/videoRepository'
import SubtitleDetailModal from '@/components/youtube-app/subtitle/SubtitleDetailModal.vue'

import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

export default {
  components: {
    SubtitleDetailModal
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

    const openModal = (subtitleTextId: string, languageCode: string) => {
      selectedSubtitleTextId.value = subtitleTextId
      selectedLanguageCode.value = languageCode
    }

    onMounted(() => {
      getVideoData()
    })
    return {
      videoData,
      subtitleList,
      selectedSubtitleTextId,
      selectedLanguageCode,
      openModal
    }
  }
}
</script>

<style scoped></style>
