SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle_info.subtitle_type = 1
ORDER BY
video_subtitle.subtitle_id ASC,
video_subtitle.t_start_ms ASC;

SELECT * FROM public.video_subtitle
JOIN video_subtitle_info
ON video_subtitle_info.subtitle_id = video_subtitle.subtitle_id
WHERE video_subtitle_info.subtitle_id = ''
ORDER BY
video_subtitle.t_start_ms ASC;