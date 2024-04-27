--手動生成字幕一括取得
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle_info.subtitle_type = 1
ORDER BY
video_subtitle.subtitle_id ASC,
video_subtitle.t_start_ms ASC;

--指定した字幕で取得
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle_info.subtitle_id = ''
ORDER BY
video_subtitle.t_start_ms ASC;

--翻訳と時間が一致しているかの確認
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle_info.subtitle_type = 1
ORDER BY
video_subtitle.t_start_ms ASC,
video_subtitle.subtitle_id DESC;

--完全一致
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle.subtitle_text='모르겠는데';

--部分一致
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle.subtitle_text LIKE '%모르겠는데%';