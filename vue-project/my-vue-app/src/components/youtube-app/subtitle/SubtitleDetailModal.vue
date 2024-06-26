<template>
  <BaseModal
    :modalTitle="'字幕詳細'"
    :actionButtonLabel="'編集'"
    :actionFunction="updateSubtitleTranslation"
  >
    <div class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="m-2">
            <label for="learningStatusDropdown" class="form-label"
              >学習ステータス</label
            >
            <DropdownSelect
              :options="learningStatus"
              v-model="selectedLearningStatus"
              @update="updateLearningStatus()"
            />
          </div>
        </div>
        <div class="col-md-4 d-flex justify-content-end">
          <div class="m-2">
            <StarIcon v-model="isFavorite" @update="updateLearningStatus()" />
          </div>
        </div>
      </div>
      <div class="m-2" v-if="subtitleTextData">
        <label for="aaa" class="form-label">タイムスタンプ付き動画リンク</label>
        <div>
          <a
            :href="
              generateTimestampUrl(
                subtitleTextData.videoId,
                subtitleTextData.tStartMs
              )
            "
            target="_blank"
            class="btn btn-link"
            ><i class="bi bi-youtube"></i>
            {{
              generateTimestampUrl(
                subtitleTextData.videoId,
                subtitleTextData.tStartMs
              )
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
import { PropType, defineComponent, ref, watchEffect } from 'vue'
import BaseModal from '@/components/common/modal/BaseModal.vue'
import subtitleRepository from '@/api/repository/subtitle-repository'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import { LearningStatusLabel } from '@/enums/learning-status'
import { showErrorToast, showSuccessToast } from '@/utils/toast-service'
import StarIcon from '@/components/common/button/StarIcon.vue'
import { generateTimestampUrl } from '@/utils/generate-timestamp-url' // 関数をインポート

export default defineComponent({
  name: 'SubtitleDetailModal',
  components: {
    BaseModal,
    DropdownSelect,
    StarIcon
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
  emits: ['update'],
  setup(props, { emit }) {
    const subtitleLiteralTranslationText = ref('')
    const subtitleTranslationTextDetail = ref('')
    const subtitleTextData = ref()

    const learningStatus = LearningStatusLabel
    const selectedLearningStatus = ref()

    const isFavorite = ref(false)

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
          isFavorite.value = response.subtitleTextData.favorite
          console.log(response)
        })
        .catch((error) => {
          showErrorToast(error)
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
          showSuccessToast('翻訳解説生成処理')
        })
        .catch((error) => {
          showErrorToast(error)
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
          showErrorToast(error)
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
          emit('update')
          showSuccessToast('字幕詳細更新処理')
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }

    const updateLearningStatus = async () => {
      subtitleRepository
        .updateLearningStatus(
          props.subtitleTextId,
          props.languageCode,
          isFavorite.value,
          selectedLearningStatus.value
        )
        .then((response) => {
          console.log(response)
          getSubtitleTextData()
          emit('update')
          showSuccessToast('学習ステータス更新処理')
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }

    watchEffect(() => {
      if (props.subtitleTextId && props.languageCode) {
        updateCancelFlag.value = true
        getSubtitleTextData()
      }
    })

    // // selectedLearningStatusの変更を監視し、変更があるたびに関数を実行
    // watch(selectedLearningStatus, () => {
    //   // 別モーダルからの遷移で更新しないように修正
    //   if (updateCancelFlag.value) {
    //     updateCancelFlag.value = false
    //   } else {
    //     updateLearningStatus()
    //   }
    // })

    return {
      updateSubtitleTranslation,
      subtitleTextData,
      subtitleLiteralTranslationText,
      subtitleTranslationTextDetail,
      learningStatus,
      selectedLearningStatus,
      executeChatgptTranslation,
      copyChatgptPrompt,
      isFavorite,
      updateLearningStatus,
      generateTimestampUrl
    }
  }
})
</script>

<style scoped></style>
