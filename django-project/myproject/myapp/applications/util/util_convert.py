import unittest


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


def milliseconds_to_timestamp(milliseconds):
    try:
        # ミリ秒を時間、分、秒に変換
        seconds = milliseconds // 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        # タイムスタンプ形式の文字列に変換
        timestamp = "{:02d}:{:02d}:{:02d}.{:03d}".format(hours, minutes, seconds, milliseconds % 1000)

        return timestamp
    except:
        # 変換できない場合は None を返す
        return None


class TestTimeConversion(unittest.TestCase):
    def test_milliseconds_to_timestamp(self):
        # ミリ秒からタイムスタンプへの変換をテスト
        test_cases = [
            (0, '00:00:00.000'),
            (1000, '00:00:01.000'),
            (10000, '00:00:10.000'),
            (60000, '00:01:00.000'),
            (131515, '00:02:11.515'),
            (3600000, '01:00:00.000'),
            (3723050, '01:02:03.050')
        ]
        for milliseconds, expected_timestamp in test_cases:
            timestamp = milliseconds_to_timestamp(milliseconds)
            self.assertEqual(timestamp, expected_timestamp)

    def test_convert_to_milliseconds(self):
        # タイムスタンプからミリ秒への変換をテスト
        test_cases = [
            ('00:00:00.000', 0),
            ('00:00:01.000', 1000),
            ('00:00:10.000', 10000),
            ('00:01:00.000', 60000),
            ('00:02:11.515', 131515),
            ('01:00:00.000', 3600000),
            ('01:02:03.050', 3723050)
        ]
        for time_str, expected_milliseconds in test_cases:
            milliseconds = convert_to_milliseconds(time_str)
            self.assertEqual(milliseconds, expected_milliseconds)


if __name__ == '__main__':
    unittest.main()
