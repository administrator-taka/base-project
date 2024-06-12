<template>
  <div class="m-2">
    <h2>頻出単語集計</h2>
    <form @submit.prevent="calculateChannelWord">
      <div class="row g-3">
        <div class="col-md-2">
          <label for="minWordInput" class="form-label">最小単語数</label>
          <input
            v-model.number="minWord"
            type="number"
            class="form-control m-2"
            id="minWordInput"
            required
          />
        </div>
        <div class="col-md-2">
          <label for="minWordLengthInput" class="form-label">最小文字数</label>
          <input
            v-model.number="minWordLength"
            type="number"
            class="form-control m-2"
            id="minWordLengthInput"
            required
          />
        </div>
        <div class="col-md-2">
          <label for="topNInput" class="form-label">上位N件</label>
          <input
            v-model.number="topN"
            type="number"
            class="form-control m-2"
            id="topNInput"
            required
          />
        </div>
        <div class="col-md-2">
          <label for="stopWordFlag" class="form-label"
            >ストップワード適用</label
          >
          <div class="form-check form-switch">
            <input
              class="form-check-input m-2"
              type="checkbox"
              id="stopWordFlag"
              v-model="stopWordFlag"
            />
            <label class="form-check-label" for="stopWordFlag">{{
              stopWordFlag ? '適用' : '適用しない'
            }}</label>
          </div>
        </div>
        <div class="col-md-2">
          <label for="subtitleTypeCodeDropdown" class="form-label"
            >字幕種類</label
          >
          <DropdownSelect :options="subtitleTypeCode" v-model="subtitleType" />
        </div>
      </div>
      <button type="submit" class="btn btn-primary m-2">
        <i class="bi bi-calculator"></i> 計算
      </button>
    </form>

    <h2>集計結果</h2>
    <div v-if="calculateWord">
      <ChartComp
        v-if="calculateWord.length > 0"
        :chartId="chartId"
        :chartData="chartData"
      />
      <div
        v-if="calculateWord.length > 0"
        class="overflow-auto"
        style="height: 1000px"
      >
        <div v-for="(word, index) in calculateWord" :key="index" class="m-2">
          <div class="row">
            <div class="col-md-8">
              <div class="m-3">
                <JsonTable :data="word" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="calculateWord.length == 0">結果がありません</div>
    </div>
  </div>
</template>
<script lang="ts">
import channelRepository from '@/api/repository/channel-repository'
import { onMounted, ref } from 'vue'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import JsonTable from '@/components/common/table/JsonTable.vue'
import { useChannelStore } from '@/store/use-channel-store'
import { SubtitleType, SubtitleTypeLabel } from '@/enums/subtitle-type'
import ChartComp from '@/components/common/graph/ChartComp.vue'
import { ChartData } from '@/interfaces/chart'
import { hexToRgba } from '@/utils/util-color' // 関数をインポート

interface ChannelWord {
  word: string
  count: number
}

export default {
  components: {
    DropdownSelect,
    JsonTable,
    ChartComp
  },
  setup() {
    const channelStore = useChannelStore()
    const subtitleTypeCode = SubtitleTypeLabel
    const subtitleType = ref<number>(SubtitleType.MANUAL)

    const minWord = ref(1)
    const minWordLength = ref(2)
    const topN = ref(50)
    const stopWordFlag = ref(false)

    const calculateWord = ref<ChannelWord[] | null>(null)
    const chartId = 'my-chart-id'

    const backgroundColorHex = '#50c1c9'
    const borderColorHex = '#2f4f4f'
    const alpha = 1 // 背景色の透明度

    // ChartData 型の chartData 変数
    const chartData = ref<ChartData>({
      labels: [], // チャートのラベル
      datasets: [
        {
          label: '頻出単語集計', // データセットのラベル
          backgroundColor: hexToRgba(backgroundColorHex, alpha), // バーの背景色
          borderColor: hexToRgba(borderColorHex, 1), // バーの境界線の色
          borderWidth: 1, // バーの境界線の幅
          data: [] // チャートに表示するデータ
        }
      ]
    })

    const calculateChannelWord = async () => {
      channelRepository
        .calculateChannelWord(
          channelStore.channelId,
          minWord.value,
          minWordLength.value,
          topN.value,
          subtitleType.value,
          stopWordFlag.value
        )
        .then((response) => {
          calculateWord.value = response.calculateWord
          console.log(response)
          const data = response.calculateWord as ChannelWord[]

          chartData.value.labels = data.map((item) => item.word)
          chartData.value.datasets[0].data = data.map((item) => item.count)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    onMounted(() => {
      calculateChannelWord()
    })

    return {
      channelStore,
      calculateChannelWord,
      minWord,
      minWordLength,
      topN,
      subtitleTypeCode,
      subtitleType,
      stopWordFlag,
      calculateWord,
      chartId,
      chartData
    }
  }
}
</script>
