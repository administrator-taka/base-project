enum SubtitleType {
  AUTOMATIC = 0, // 自動字幕
  MANUAL = 1 // 手動字幕
}

const SubtitleTypeLabel: { name: string; value: number }[] = [
  { name: '自動字幕', value: SubtitleType.AUTOMATIC },
  {
    name: '手動字幕',
    value: SubtitleType.MANUAL
  }
]

export { SubtitleType, SubtitleTypeLabel }
