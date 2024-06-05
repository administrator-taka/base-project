<template>
  <div>
    <Bar :id="chartId" :options="chartOptions" :data="chartData" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
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

export default {
  props: {
    chartId: {
      type: String,
      default: 'my-chart-id'
    },
    chartData: {
      type: Object,
      default: () => ({
        labels: [],
        datasets: [{ data: [] }]
      })
    },
    chartOptions: {
      type: Object,
      default: () => ({
        responsive: true
      })
    }
  },
  components: { Bar }
}
</script>

<style scoped></style>
