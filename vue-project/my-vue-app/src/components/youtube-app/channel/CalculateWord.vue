<template>
  <div class="m-2">
    <h2>頻出単語集計</h2>
    <form @submit.prevent="calculateChannelWord">
      <div class="row g-3">
        <div class="col-md-3">
          <label for="minWordInput" class="form-label">最小単語数</label>
          <input
            v-model.number="minWord"
            type="number"
            class="form-control m-2"
            id="minWordInput"
            placeholder="最小単語数"
            required
          />
        </div>
        <div class="col-md-3">
          <label for="minWordLengthInput" class="form-label"
            >最小単語の長さ</label
          >
          <input
            v-model.number="minWordLength"
            type="number"
            class="form-control m-2"
            id="minWordLengthInput"
            placeholder="最小単語の長さ"
            required
          />
        </div>
        <div class="col-md-3">
          <label for="topNInput" class="form-label">上位N件</label>
          <input
            v-model.number="topN"
            type="number"
            class="form-control m-2"
            id="topNInput"
            placeholder="上位N件"
            required
          />
        </div>
        <div class="col-md-3">
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

    <div v-if="calculateWord" class="m-2">
      <h2>集計結果</h2>
      <ChartComp
        :chartId="chartId"
        :chartData="chartData"
        :chartOptions="chartOptions"
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
import { ref } from 'vue'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import JsonTable from '@/components/common/table/JsonTable.vue'
import { useChannelStore } from '@/store/use-channel-store'
import { SubtitleType, SubtitleTypeLabel } from '@/enums/subtitle-type'
import ChartComp from '@/components/common/graph/ChartComp.vue'

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

    const minWord = ref(1)
    const minWordLength = ref(2)
    const topN = ref(50)
    const subtitleTypeCode = SubtitleTypeLabel
    const subtitleType = ref<number>(SubtitleType.MANUAL)
    const calculateWord = ref()
    const chartId = 'my-chart-id'
    const chartData = ref({
      labels: [] as string[],
      datasets: [
        {
          label: '頻出単語集計',
          backgroundColor: 'rgba(0, 163, 175, 0.2)',
          borderColor: 'rgba(0, 163, 175, 1)',
          borderWidth: 1,
          data: [] as number[]
        }
      ]
    })
    const chartOptions = {
      responsive: true
    }

    const calculateChannelWord = async () => {
      channelRepository
        .calculateChannelWord(
          channelStore.channelId,
          minWord.value,
          minWordLength.value,
          topN.value,
          subtitleType.value
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

    return {
      channelStore,
      calculateChannelWord,
      minWord,
      minWordLength,
      topN,
      subtitleTypeCode,
      subtitleType,
      calculateWord,
      chartId,
      chartData,
      chartOptions
    }
  }
}
</script>

<style scoped></style>
