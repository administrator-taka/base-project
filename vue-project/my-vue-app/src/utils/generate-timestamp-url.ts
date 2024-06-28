export function generate_timestamp_url(
  videoId: string,
  timestamp: number
): string {
  return 'https://www.youtube.com/watch?v=' + videoId + '&t=' + timestamp + 'ms'
}
