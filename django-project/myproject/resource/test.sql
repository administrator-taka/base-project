--手動生成字幕一括取得
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle_info.subtitle_type = 1
ORDER BY
video_subtitle.subtitle_id ASC,
video_subtitle.t_start_ms ASC
LIMIT 100
;

--指定した字幕で取得
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle_info.subtitle_id = ''
ORDER BY
video_subtitle.t_start_ms ASC
LIMIT 100
;

--翻訳と時間が一致しているかの確認
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle_info.subtitle_type = 1
ORDER BY
video_subtitle.t_start_ms ASC,
video_subtitle.subtitle_id DESC
LIMIT 100
;

--完全一致
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle.subtitle_text='모르겠는데'
LIMIT 100
;

--部分一致
SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle.subtitle_text LIKE '%모르겠는데%'
LIMIT 100
;

--出現度ランキング
SELECT subtitle_text, COUNT(*) AS subtitle_count
FROM video_subtitle
GROUP BY subtitle_text
ORDER BY subtitle_count DESC
LIMIT 100
;

--出現度ランキング（言語指定、自動指定：手動だと歌詞などで不自然な集計が行われるため）
SELECT subtitle_text, COUNT(*) AS subtitle_count
FROM video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle_info.language_code='ko'
AND subtitle_type=0
GROUP BY subtitle_text
ORDER BY subtitle_count DESC
LIMIT 100
;

--初期データ
"UCHE7GBQVtdh-c1m3tjFdevQ","ko","{ja}"


--字幕データ整形

select * from
video_subtitle_info
join video_subtitle
on video_subtitle_info.subtitle_id=video_subtitle.subtitle_id
left join subtitle_translation
on video_subtitle.subtitle_text_id=subtitle_translation.subtitle_text_id
where video_subtitle_info.subtitle_type=1
and video_subtitle_info.video_id='dU_coAmDBmc'
order by video_subtitle.t_start_ms,
video_subtitle_info.language_code desc
LIMIT 100
;
--検索
select * from video_detail
join video_subtitle_info
on video_detail.video_id=video_subtitle_info.video_id
join video_subtitle
on video_subtitle.subtitle_id=video_subtitle_info.subtitle_id
WHERE video_subtitle_info.subtitle_type=0
ORDER BY
video_subtitle_info.language_code,
video_subtitle_info.video_id,
video_subtitle.t_start_ms,
video_subtitle.t_offset_ms
LIMIT 100
;


--データ確認
SELECT relname,n_live_tup
FROM pg_stat_user_tables
WHERE n_live_tup > 0;

--動画情報更新用
update video_detail
set e_tag='test';

--字幕詳細削除用
DELETE FROM subtitle_translation
USING video_subtitle
WHERE video_subtitle.subtitle_text_id = subtitle_translation.subtitle_text_id
AND video_subtitle.subtitle_id = 'E2r9u5l0Y6k1en';