<template>
  <BaseModal
    :modalTitle="'字幕詳細'"
    :actionButtonLabel="'編集'"
    :actionFunction="updateSubtitleTranslation"
  >
    <div class="container">
      <div class="m-2">
        <label for="learningStatusDropdown" class="form-label"
          >学習ステータス</label
        >
        <DropdownSelect
          :options="learningStatus"
          v-model="selectedLearningStatus"
        />
      </div>
      <div class="m-2" v-if="subtitleTextData">
        <label for="aaa" class="form-label">タイムスタンプ付き動画リンク</label>
        <div>
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
            ><i class="bi bi-youtube"></i>
            {{
              'https://www.youtube.com/watch?v=' +
              subtitleTextData.videoId +
              '&t=' +
              subtitleTextData.tStartMs +
              'ms'
            }}
          </a>
        </div>
      </div>
      <div class="m-2">
        <label for="aaa" class="form-label">字幕</label>
        <input
          type="text"
          class="form-control"
          :value="subtitleTextData ? subtitleTextData.subtitleText : ''"
          disabled
        />
      </div>
      <div class="m-2">
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
      <div class="m-2">
        <label for="subtitleLiteralTranslationText" class="form-label"
          >直訳</label
        >
        <input
          type="text"
          id="subtitleLiteralTranslationText"
          class="form-control"
          v-model="subtitleLiteralTranslationText"
        />
      </div>
      <div class="m-2">
        <label for="subtitleTranslationTextDetail" class="form-label"
          >翻訳詳細</label
        >
        <button @click="copyChatgptPrompt" class="btn btn-light m-2">
          <i class="bi bi-clipboard"></i> プロンプトのコピー
        </button>
        <button
          @click="executeChatgptTranslation"
          class="btn btn-warning m-2"
          :disabled="!!subtitleTranslationTextDetail"
        >
          <i class="bi bi-exclamation-triangle"></i> ChatGPTで解説生成
        </button>
        <textarea
          id="subtitleTranslationTextDetail"
          class="form-control"
          v-model="subtitleTranslationTextDetail"
          :rows="
            subtitleTranslationTextDetail
              ? subtitleTranslationTextDetail.split('\n').length + 2
              : 3
          "
        ></textarea>
      </div>
    </div>
  </BaseModal>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, watch, watchEffect } from 'vue'
import BaseModal from '@/components/common/modal/BaseModal.vue'
import subtitleRepository from '@/api/repository/subtitle-repository'
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
    const selectedLearningStatus = ref()

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
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const executeChatgptTranslation = async () => {
      subtitleRepository
        .executeChatgptTranslation(
          props.subtitleTextId,
          props.languageCode,
          true
        )
        .then((response) => {
          console.log(response)
          subtitleTranslationTextDetail.value = response.chatgptData.response
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const copyChatgptPrompt = async () => {
      subtitleRepository
        .executeChatgptTranslation(
          props.subtitleTextId,
          props.languageCode,
          false
        )
        .then((response) => {
          console.log(response)
          const request = response.chatgptData.request // リクエストを取得
          // クリップボードにテキストをコピー
          navigator.clipboard
            .writeText(request)
            .then(() => {
              console.log('クリップボードにコピーされました')
              // コピー成功時の処理を追加することもできます
            })
            .catch((error) => {
              console.error(
                'クリップボードの操作中にエラーが発生しました:',
                error
              )
            })
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const updateCancelFlag = ref(false)

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
        updateCancelFlag.value = true
        getSubtitleTextData()
      }
    })

    // selectedLearningStatusの変更を監視し、変更があるたびに関数を実行
    watch(selectedLearningStatus, () => {
      // 別モーダルからの遷移で更新しないように修正
      if (updateCancelFlag.value) {
        updateCancelFlag.value = false
      } else {
        updateLearningStatus()
      }
    })

    return {
      updateSubtitleTranslation,
      subtitleTextData,
      subtitleLiteralTranslationText,
      subtitleTranslationTextDetail,
      learningStatus,
      selectedLearningStatus,
      executeChatgptTranslation,
      copyChatgptPrompt
    }
  }
})
</script>

<style scoped></style>
