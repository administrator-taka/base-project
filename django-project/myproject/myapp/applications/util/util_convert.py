def convert_to_milliseconds(time_str):
    try:
        # 時間文字列を時、分、秒、ミリ秒に分割
        h, m, s_ms = time_str.split(':')
        s, ms = s_ms.split('.')
        # 時間、分、秒、ミリ秒を整数に変換してミリ秒に変換
        milliseconds = int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)
        return milliseconds
    except:
        # 変換できない場合は None を返す
        return None
