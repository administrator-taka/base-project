import unittest
from datetime import datetime
from enum import Enum

from pytz import timezone


class TimeZone(Enum):
    UTC = 'UTC'
    JST = 'Asia/Tokyo'  # 日本
    KST = 'Asia/Seoul'  # 韓国
    CST = 'Asia/Shanghai'  # 中国
    WIB = 'Asia/Jakarta'  # インドネシア (西部インドネシア時間)
    ICT = 'Asia/Bangkok'  # タイ
    IST = 'Asia/Kolkata'  # インド
    MYT = 'Asia/Kuala_Lumpur'  # マレーシア
    PHT = 'Asia/Manila'  # フィリピン
    SGT = 'Asia/Singapore'  # シンガポール
    AWST = 'Australia/Perth'  # オーストラリア (西部標準時)
    AEST = 'Australia/Sydney'  # オーストラリア (東部標準時)
    NZST = 'Pacific/Auckland'  # ニュージーランド (標準時)
    # 追加のタイムゾーンをここに追加できます


def convert_to_timezone(utc_time, target_timezone):
    utc_time = timezone(TimeZone.UTC.value).localize(utc_time)
    target_time = utc_time.astimezone(timezone(target_timezone.value))
    return target_time


class TestTimeZoneConversion(unittest.TestCase):

    def test_utc_to_jst(self):
        utc_time = datetime(2024, 4, 21, 12, 0, 0)
        jst_time = convert_to_timezone(utc_time, TimeZone.JST)
        self.assertEqual(jst_time.hour, 21)  # Japan is 9 hours ahead of UTC at this time

    def test_utc_to_kst(self):
        utc_time = datetime(2024, 4, 21, 12, 0, 0)
        kst_time = convert_to_timezone(utc_time, TimeZone.KST)
        self.assertEqual(kst_time.hour, 21)  # Korea is 9 hours ahead of UTC at this time

    def test_utc_to_cst(self):
        utc_time = datetime(2024, 4, 21, 12, 0, 0)
        cst_time = convert_to_timezone(utc_time, TimeZone.CST)
        self.assertEqual(cst_time.hour, 20)  # China is 8 hours ahead of UTC at this time


if __name__ == '__main__':
    unittest.main()
