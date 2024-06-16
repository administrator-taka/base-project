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
          <div class="row">
            <div class="col-md-4">
              <img
                :src="subtitle.thumbnail"
                alt="Image"
                class="img-thumbnail m-2"
              />
            </div>
            <div class="col-md-6">
              <JsonTable :data="subtitle" />
            </div>
            <div class="col-md-2">
              <button
                type="button"
                class="btn btn-primary m-2"
                @click="
                  openModal(subtitle.subtitleTextId, subtitle.languageCode)
                "
                data-bs-toggle="modal"
                data-bs-target="#exampleModal"
              >
                字幕詳細
              </button>
              <button
                @click="goToVideoPage(subtitle.videoId)"
                class="btn btn-info m-2"
              >
                動画詳細
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="favoriteSubtitleList">
        <h2>お気に入り</h2>
        <div v-for="(subtitle, index) in favoriteSubtitleList" :key="index">
          <div class="row">
            <div class="col-md-4">
              <img
                :src="subtitle.thumbnail"
                alt="Image"
                class="img-thumbnail m-2"
              />
            </div>
            <div class="col-md-6">
              <JsonTable :data="subtitle" />
            </div>
            <div class="col-md-2">
              <button
                type="button"
                class="btn btn-primary m-2"
                @click="
                  openModal(subtitle.subtitleTextId, subtitle.languageCode)
                "
                data-bs-toggle="modal"
                data-bs-target="#exampleModal"
              >
                字幕詳細
              </button>
              <button
                @click="goToVideoPage(subtitle.videoId)"
                class="btn btn-info m-2"
              >
                動画詳細
              </button>
            </div>
          </div>
        </div>
      </div>
      <SubtitleDetailModal
        :subtitleTextId="selectedModalSubtitleTextId"
        :languageCode="selectedModalLanguageCode"
        @update="
          () => {
            getLearningSubtitleList()
            getFavoriteSubtitleList()
          }
        "
      />
    </main>
  </div>
</template>

<script lang="ts">
import learningLanguageMemoryRepository from '@/api/repository/learning-language-memory-repository'
import { onMounted, ref, watch } from 'vue'
import SubtitleDetailModal from '@/components/youtube-app/subtitle/SubtitleDetailModal.vue'
import { YouTubeLanguage, YouTubeLanguageLabel } from '@/enums/youtube-language'
import { LearningStatus, LearningStatusLabel } from '@/enums/learning-status'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import router from '@/router'
import JsonTable from '@/components/common/table/JsonTable.vue'
import { showErrorToast } from '@/utils/toast-service'

export default {
  components: {
    SubtitleDetailModal,
    DropdownSelect,
    JsonTable
  },
  setup() {
    const learningSubtitleList = ref()
    const favoriteSubtitleList = ref()
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
          showErrorToast(error)
        })
    }

    const getFavoriteSubtitleList = async () => {
      learningLanguageMemoryRepository
        .getFavoriteSubtitleList(selectedLanguageCode.value)
        .then((response) => {
          favoriteSubtitleList.value = response.favoriteSubtitleList
          console.log(response)
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }
    const goToVideoPage = (videoId: string) => {
      router.push(`/video/${videoId}`)
    }

    onMounted(() => {
      getLearningSubtitleList()
      getFavoriteSubtitleList()
    })

    // selectedLanguageCode か selectedLearningStatus が変更されたら、自動的に字幕リストを更新する
    watch([selectedLanguageCode, selectedLearningStatus], () => {
      getLearningSubtitleList()
      getFavoriteSubtitleList()
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
      goToVideoPage,
      getLearningSubtitleList,
      getFavoriteSubtitleList,
      favoriteSubtitleList
    }
  }
}
</script>

<style scoped></style>
