<template>
  <div>
    <Bar :id="chartId" :data="chartData" />
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
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
  components: { Bar }
})
</script>
