// @/interfaces/chart.ts

export interface ChartData {
  labels: string[]
  datasets: ChartDataset[]
}

export interface ChartDataset {
  label?: string
  data: number[]
  backgroundColor?: string
  borderColor?: string
  borderWidth?: number
}
