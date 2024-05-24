<template>
  <BaseModal
    :modalTitle="'字幕詳細'"
    :actionButtonLabel="'編集'"
    :actionFunction="updateSubtitleTranslation"
  >
    <div class="container">
      <div class="mb-3">
        <label for="learningStatusDropdown" class="form-label"
          >学習ステータス</label
        >
        <DropdownSelect
          :options="learningStatus"
          v-model="selectedLearningStatus"
        />
      </div>
      <pre>{{ JSON.stringify(subtitleTextData, null, 2) }}</pre>
      <div v-if="subtitleTextData">
        <a
          :href="
            'https://www.youtube.com/watch?v=' +
            subtitleTextData.videoId +
            '&t=' +
            subtitleTextData.tStartMs +
            'ms'
          "
          target="_blank"
          class="btn btn-link"
        >
          {{
            'https://www.youtube.com/watch?v=' +
            subtitleTextData.videoId +
            '&t=' +
            subtitleTextData.tStartMs +
            'ms'
          }}
        </a>
      </div>
      <div class="mb-3">
        <label for="aaa" class="form-label">字幕</label>
        <input
          type="text"
          class="form-control"
          :value="subtitleTextData ? subtitleTextData.subtitleText : ''"
          disabled
        />
      </div>
      <div class="mb-3">
        <label for="bbb" class="form-label">翻訳</label>
        <input
          type="text"
          class="form-control"
          :value="
            subtitleTextData ? subtitleTextData.subtitleTranslationText : ''
          "
          disabled
        />
      </div>
      <div class="mb-3">
        <label for="subtitleLiteralTranslationText" class="form-label"
          >字幕翻訳テキスト</label
        >
        <input
          type="text"
          id="subtitleLiteralTranslationText"
          class="form-control"
          v-model="subtitleLiteralTranslationText"
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
          rows="6"
        ></textarea>
      </div>
    </div>
  </BaseModal>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, watch, watchEffect } from 'vue'
import BaseModal from '@/components/common/modal/BaseModal.vue'
import subtitleRepository from '@/api/repository/subtitleRepository'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import { LearningStatusLabel } from '@/enums/learning-status'

export default defineComponent({
  name: 'SubtitleDetailModal',
  components: {
    BaseModal,
    DropdownSelect
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
    const subtitleLiteralTranslationText = ref('')
    const subtitleTranslationTextDetail = ref('')
    const subtitleTextData = ref()

    const learningStatus = LearningStatusLabel
    const selectedLearningStatus = ref(0)

    const getSubtitleTextData = async () => {
      subtitleRepository
        .getSubtitleTextData(props.subtitleTextId, props.languageCode)
        .then((response) => {
          subtitleTextData.value = response.subtitleTextData
          subtitleLiteralTranslationText.value =
            response.subtitleTextData.subtitleLiteralTranslationText
          subtitleTranslationTextDetail.value =
            response.subtitleTextData.subtitleTranslationTextDetail
          selectedLearningStatus.value = parseInt(
            response.subtitleTextData.learningStatus
          )
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
          subtitleLiteralTranslationText.value,
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

    const updateLearningStatus = async () => {
      subtitleRepository
        .updateLearningStatus(
          props.subtitleTextId,
          props.languageCode,
          selectedLearningStatus.value
        )
        .then((response) => {
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

    // selectedLearningStatusの変更を監視し、変更があるたびに関数を実行
    watch(selectedLearningStatus, () => {
      updateLearningStatus()
    })

    return {
      updateSubtitleTranslation,
      subtitleTextData,
      subtitleLiteralTranslationText,
      subtitleTranslationTextDetail,
      learningStatus,
      selectedLearningStatus
    }
  }
})
</script>

<style scoped></style>
