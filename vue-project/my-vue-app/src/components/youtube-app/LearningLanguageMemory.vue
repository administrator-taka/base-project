<template>
  <div>
    <main class="main-content">
      <h1>言語学習記録確認画面</h1>
      <div class="row g-3">
        <div class="col-md-3">
          <label for="languageCodeDropdown" class="form-label"
            ><i class="bi bi-globe"></i> 学習言語</label
          >
          <DropdownSelect
            :options="languageCode"
            v-model="selectedLanguageCode"
          />
        </div>
        <div class="col-md-3">
          <label for="learningStatusDropdown" class="form-label"
            ><i class="bi bi-pencil"></i> 学習ステータス</label
          >
          <DropdownSelect
            :options="learningStatus"
            v-model="selectedLearningStatus"
          />
        </div>
      </div>
      <div v-if="learningSubtitleList">
        <h2>字幕一覧</h2>
        <div v-for="(subtitle, index) in learningSubtitleList" :key="index">
          <img :src="subtitle.thumbnail" alt="Image" class="img-thumbnail" />
          <button
            type="button"
            class="btn btn-primary"
            @click="openModal(subtitle.subtitleTextId, subtitle.languageCode)"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
          >
            字幕詳細
          </button>
          <button @click="goToVideoPage(subtitle.videoId)" class="btn btn-info">
            動画ページへ
          </button>
          <JsonTable :data="subtitle" />
        </div>
      </div>
      <SubtitleDetailModal
        :subtitleTextId="selectedModalSubtitleTextId"
        :languageCode="selectedModalLanguageCode"
      />
    </main>
  </div>
</template>

<script lang="ts">
import learningLanguageMemoryRepository from '@/api/repository/learningLanguageMemoryRepository'
import { onMounted, ref, watch } from 'vue'
import SubtitleDetailModal from '@/components/youtube-app/subtitle/SubtitleDetailModal.vue'
import { YouTubeLanguage, YouTubeLanguageLabel } from '@/enums/youtube-language'
import { LearningStatus, LearningStatusLabel } from '@/enums/learning-status'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import router from '@/router'
import JsonTable from '@/components/common/table/JsonTable.vue'

export default {
  components: {
    SubtitleDetailModal,
    DropdownSelect,
    JsonTable
  },
  setup() {
    const learningSubtitleList = ref()
    const selectedModalSubtitleTextId = ref<string>('')
    const selectedModalLanguageCode = ref<string>('')

    const languageCode = YouTubeLanguageLabel
    const selectedLanguageCode = ref<string>(YouTubeLanguage.KOREAN)

    const learningStatus = LearningStatusLabel
    const selectedLearningStatus = ref(LearningStatus.ONE_WORD_UNKNOWN)

    const openModal = (subtitleTextId: string, languageCode: string) => {
      selectedModalSubtitleTextId.value = subtitleTextId
      selectedModalLanguageCode.value = languageCode
    }

    const getLearningSubtitleList = async () => {
      learningLanguageMemoryRepository
        .getLearningSubtitleList(
          selectedLanguageCode.value,
          selectedLearningStatus.value
        )
        .then((response) => {
          learningSubtitleList.value = response.learningSubtitleList
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }
    const goToVideoPage = (videoId: string) => {
      router.push(`/video/${videoId}`)
    }

    onMounted(() => {
      getLearningSubtitleList()
    })

    // selectedLanguageCode か selectedLearningStatus が変更されたら、自動的に字幕リストを更新する
    watch([selectedLanguageCode, selectedLearningStatus], () => {
      getLearningSubtitleList()
    })

    return {
      learningSubtitleList,
      selectedModalSubtitleTextId,
      selectedModalLanguageCode,
      openModal,
      languageCode,
      selectedLanguageCode,
      learningStatus,
      selectedLearningStatus,
      goToVideoPage
    }
  }
}
</script>

<style scoped></style>
