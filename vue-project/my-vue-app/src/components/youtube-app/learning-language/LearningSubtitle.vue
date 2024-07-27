<template>
  <div>
    <h1>ベース言語管理</h1>
    <div v-if="baseLanguages.length">
      <h2>ベース言語一覧</h2>
      <div
        v-for="(baseLanguage, index) in baseLanguages"
        :key="index"
        class="m-2"
      >
        <JsonTable :data="baseLanguage" />
      </div>
    </div>
    <div>
      <h2>新しいベース言語を作成</h2>
      <form @submit.prevent="createLanguage">
        <DropdownSelect
          :options="languageCode"
          v-model="selectedLanguageCode"
        />
        <div class="col-md-6">
          <input
            v-model="newDocuments"
            type="text"
            class="form-control"
            placeholder="ドキュメント"
            required
          />
        </div>
        <div class="col-md-6">
          <input
            v-model="learningLanguageDocuments"
            type="text"
            class="form-control"
            placeholder="学習言語ドキュメント"
          />
        </div>
        <div class="col-md-6">
          <input
            v-model="learningLanguageExplanation"
            type="text"
            class="form-control"
            placeholder="学習言語説明"
          />
        </div>
        <div class="col-md-6">
          <input
            v-model="learningLanguageVideoId"
            type="text"
            class="form-control"
            placeholder="学習言語動画ID"
          />
        </div>
        <div class="col-md-6">
          <input
            v-model="learningLanguageTimestampMs"
            type="number"
            class="form-control"
            placeholder="学習言語タイムスタンプ (ms)"
          />
        </div>
        <label>
          <input type="checkbox" v-model="newIsPublished" />
          公開する
        </label>
        <button type="submit" class="btn btn-primary m-2">作成</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import learningLanguageMemoryRepository from '@/api/repository/learning-language-memory-repository'
import JsonTable from '@/components/common/table/JsonTable.vue'
import { YouTubeLanguage, YouTubeLanguageLabel } from '@/enums/youtube-language'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import { showErrorToast } from '@/utils/toast-service'

export default {
  components: {
    JsonTable,
    DropdownSelect
  },
  setup() {
    const baseLanguages = ref([])

    const newDocuments = ref('')
    const newIsPublished = ref(false)
    const learningLanguageDocuments = ref('')
    const learningLanguageExplanation = ref('')
    const learningLanguageVideoId = ref('')
    const learningLanguageTimestampMs = ref<number>()
    const languageCode = YouTubeLanguageLabel
    const selectedLanguageCode = ref<string>(YouTubeLanguage.KOREAN)
    const getBaseLanguageList = async () => {
      await learningLanguageMemoryRepository
        .getBaseLanguageList()
        .then((response) => {
          console.log(response)
          baseLanguages.value = response.baseLanguageList
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }

    const createLanguage = async () => {
      await learningLanguageMemoryRepository
        .createBaseLanguage(
          selectedLanguageCode.value,
          newDocuments.value,
          newIsPublished.value,
          learningLanguageDocuments.value,
          learningLanguageExplanation.value,
          learningLanguageVideoId.value,
          learningLanguageTimestampMs.value
        )
        .then((response) => {
          getBaseLanguageList()
          console.log(response)
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }

    onMounted(() => {
      getBaseLanguageList()
    })

    return {
      baseLanguages,
      newDocuments,
      newIsPublished,
      learningLanguageDocuments,
      learningLanguageExplanation,
      learningLanguageVideoId,
      learningLanguageTimestampMs,
      createLanguage,
      languageCode,
      selectedLanguageCode
    }
  }
}
</script>

<style scoped>
/* スタイルを追加 */
</style>
