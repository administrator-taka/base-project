<template>
  <div>
    <main class="main-content">
      <h1>ベース言語管理</h1>
      <CreateBaseLanguage
        @createBaseLanguage="getBaseLanguageList()"
      ></CreateBaseLanguage>
      <div v-if="baseLanguages">
        <h2>ベース言語一覧</h2>
        <div
          v-for="(baseLanguage, index) in baseLanguages"
          :key="index"
          class="m-2"
        >
          <RangeSelector
            @range-selected="goToBaseLanguagePage(baseLanguage.baseLanguageId)"
          >
            <div class="m-3">
              <!-- TODO:モーダル修正後に削除 -->
              <div style="height: 1rem"></div>
              <JsonTable :data="baseLanguage" />
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
import CreateBaseLanguage from '@/components/youtube-app/learning-language/CreateBaseLanguage.vue'
import RangeSelector from '@/components/common/button/RangeSelector.vue'
import router from '@/router'

export default {
  components: {
    JsonTable,
    DropdownSelect,
    CreateBaseLanguage,
    RangeSelector
  },
  setup() {
    const baseLanguages = ref()

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

    onMounted(() => {
      getBaseLanguageList()
    })
    const goToBaseLanguagePage = (baseLanguageId: string) => {
      router.push(`/base-language/${baseLanguageId}`)
    }
    return {
      baseLanguages,
      getBaseLanguageList,
      goToBaseLanguagePage
    }
  }
}
</script>

<style scoped>
/* スタイルを追加 */
</style>
