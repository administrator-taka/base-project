--手動生成字幕一括取得
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_info_id
WHERE video_subtitle_info.subtitle_type = 1
ORDER BY
video_subtitle.subtitle_info_id ASC,
video_subtitle.t_start_ms ASC;

--指定した字幕で取得
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_info_id
WHERE video_subtitle_info.subtitle_id = ''
ORDER BY
video_subtitle.t_start_ms ASC;

--翻訳と時間が一致しているかの確認
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_info_id
WHERE video_subtitle_info.subtitle_type = 1
ORDER BY
video_subtitle.t_start_ms ASC,
video_subtitle.subtitle_info_id DESC;

--完全一致
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_info_id
WHERE video_subtitle.subtitle_text='모르겠는데';

--部分一致
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_info_id
WHERE video_subtitle.subtitle_text LIKE '%모르겠는데%';

--出現度ランキング
SELECT subtitle_text, COUNT(*) AS subtitle_count
FROM video_subtitle
GROUP BY subtitle_text
ORDER BY subtitle_count DESC;

--出現度ランキング（言語指定、自動指定：手動だと歌詞などで不自然な集計が行われるため）
SELECT subtitle_text, COUNT(*) AS subtitle_count
FROM video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_info_id
WHERE video_subtitle_info.language_code='ko'
AND subtitle_type=0
GROUP BY subtitle_text
ORDER BY subtitle_count DESC;

--初期データ
"UCHE7GBQVtdh-c1m3tjFdevQ","ko","{ja}"