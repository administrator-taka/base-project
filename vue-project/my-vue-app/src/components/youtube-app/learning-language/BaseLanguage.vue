<template>
  <div>
    <main class="main-content">
      <h1>学習言語管理</h1>
      <CreateLearningLanguage
        @createLearningLanguage="getBaseLanguageDetail()"
      ></CreateLearningLanguage>
      <div v-if="baseLanguage">
        <JsonTable :data="baseLanguage.baseLanguageData"></JsonTable>
        <div
          v-for="(
            learningLanguage, index
          ) in baseLanguage.learningLanguagesData"
          :key="index"
        >
          <RangeSelector
            @range-selected="
              goToLearningLanguagePage(learningLanguage.learningLanguageId)
            "
          >
            <div class="m-3">
              <!-- TODO:モーダル修正後に削除 -->
              <div style="height: 1rem"></div>
              <JsonTable :data="learningLanguage" />
            </div>
          </RangeSelector>
        </div>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import learningLanguageMemoryRepository from '@/api/repository/learning-language-memory-repository'
import JsonTable from '@/components/common/table/JsonTable.vue'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import { showErrorToast } from '@/utils/toast-service'
import CreateLearningLanguage from '@/components/youtube-app/learning-language/CreateLearningLanguage.vue'
import RangeSelector from '@/components/common/button/RangeSelector.vue'
import router from '@/router'
import { useRoute } from 'vue-router'

export default {
  components: {
    JsonTable,
    DropdownSelect,
    CreateLearningLanguage,
    RangeSelector
  },
  setup() {
    const route = useRoute()
    const baseLanguageId = ref<string>(
      typeof route.params.baseLanguageId === 'string'
        ? route.params.baseLanguageId
        : ''
    )
    const baseLanguage = ref()
    const getBaseLanguageDetail = async () => {
      await learningLanguageMemoryRepository
        .getBaseLanguageDetail(baseLanguageId.value)
        .then((response) => {
          console.log(response)
          baseLanguage.value = response.baseLanguageDetail
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }

    onMounted(() => {
      getBaseLanguageDetail()
    })
    const goToLearningLanguagePage = (learningLanguageId: string) => {
      router.push(`/learning-subtitle-language/${learningLanguageId}`)
    }
    return {
      getBaseLanguageDetail,
      baseLanguage,
      goToLearningLanguagePage
    }
  }
}
</script>

<style scoped>
/* スタイルを追加 */
</style>
