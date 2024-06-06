<template>
  <div>
    <Bar :id="chartId" :data="copiedChartData" :key="shouldRedrawChart" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, shallowReactive, watch } from 'vue'
import { Bar } from 'vue-chartjs'
import { ChartData } from '@/interfaces/chart'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default defineComponent({
  props: {
    chartId: {
      type: String,
      default: 'my-chart-id'
    },
    chartData: {
      type: Object as () => ChartData,
      default: () => ({
        labels: [],
        datasets: [{ data: [] }]
      })
    }
  },
  setup(props) {
    const copiedChartData = shallowReactive({ ...props.chartData })
    const shouldRedrawChart = ref(false)

    // chartData の変更を監視し、変更があればグラフを再描画する
    watch(
      () => props.chartData.labels,
      () => {
        shouldRedrawChart.value = !shouldRedrawChart.value
      }
    )

    watch(
      () => props.chartData.datasets,
      () => {
        shouldRedrawChart.value = !shouldRedrawChart.value
      }
    )

    return {
      copiedChartData,
      shouldRedrawChart
    }
  },
  components: {
    Bar
  }
})
</script>
