<template>
  <BaseModal
    :modalTitle="'字幕詳細'"
    :actionButtonLabel="'編集'"
    :actionFunction="updateSubtitleTranslation"
  >
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <p>字幕ID: {{ subtitleTextId }}</p>
          <p>言語コード: {{ languageCode }}</p>
          <pre>{{ JSON.stringify(subtitleTextData, null, 2) }}</pre>
        </div>
        <div class="col-md-6">
          <div class="mb-3">
            <label for="subtitleTranslationText" class="form-label"
              >字幕翻訳テキスト</label
            >
            <input
              type="text"
              id="subtitleTranslationText"
              class="form-control"
              v-model="subtitleTranslationText"
              required
            />
          </div>
          <div class="mb-3">
            <label for="subtitleTranslationTextDetail" class="form-label"
              >字幕翻訳詳細</label
            >
            <textarea
              id="subtitleTranslationTextDetail"
              class="form-control"
              v-model="subtitleTranslationTextDetail"
              required
            ></textarea>
          </div>
        </div>
      </div>
    </div>
  </BaseModal>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, watchEffect } from 'vue'
import BaseModal from '@/components/common/modal/BaseModal.vue'
import subtitleRepository from '@/api/repository/subtitleRepository'

export default defineComponent({
  name: 'SubtitleDetailModal',
  components: {
    BaseModal
  },
  props: {
    subtitleTextId: {
      type: String as PropType<string>,
      required: true
    },
    languageCode: {
      type: String as PropType<string>,
      required: true
    }
  },
  setup(props) {
    const subtitleTranslationText = ref('')
    const subtitleTranslationTextDetail = ref('')
    const subtitleTextData = ref()

    const getSubtitleTextData = async () => {
      subtitleRepository
        .getSubtitleTextData(props.subtitleTextId, props.languageCode)
        .then((response) => {
          subtitleTextData.value = response.subtitleTextData
          // Set initial values for the form fields
          subtitleTranslationText.value =
            response.subtitleTextData.subtitleTranslationText
          subtitleTranslationTextDetail.value =
            response.subtitleTextData.subtitleTranslationTextDetail
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const updateSubtitleTranslation = async () => {
      subtitleRepository
        .updateSubtitleTranslation(
          props.subtitleTextId,
          props.languageCode,
          subtitleTranslationText.value,
          subtitleTranslationTextDetail.value
        )
        .then((response) => {
          subtitleTextData.value = response.subtitleTextData
          console.log(response)
          getSubtitleTextData()
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    watchEffect(() => {
      if (props.subtitleTextId && props.languageCode) {
        getSubtitleTextData()
      }
    })
    return {
      updateSubtitleTranslation,
      subtitleTextData,
      subtitleTranslationText,
      subtitleTranslationTextDetail
    }
  }
})
</script>

<style scoped></style>
