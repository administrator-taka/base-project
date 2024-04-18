class TimestampConverter:
    def __init__(self, timestamp: str = "", seconds: float = 0.0) -> None:
        self.timestamp: str = timestamp
        self.seconds: float = seconds

    def from_timestamp_to_seconds(self) -> float:
        if not self.timestamp:
            return 0.0

        # タイムスタンプを [hours, minutes, seconds] のリストに分割
        parts = self.timestamp.split(":")
        if len(parts) == 3:
            hours, minutes, seconds = map(float, parts)
        elif len(parts) == 2:
            hours = 0
            minutes, seconds = map(float, parts)
        else:
            return float(self.timestamp)  # タイムスタンプが秒数のみの場合

        # 経過秒数に変換
        total_seconds = hours * 3600 + minutes * 60 + seconds
        self.seconds = total_seconds
        return total_seconds

    def from_seconds_to_timestamp(self) -> str:
        if self.seconds == 0.0:
            return "00:00:00.000"

        # 時間、分、秒に変換
        hours = int(self.seconds) // 3600
        remaining_seconds = self.seconds % 3600
        minutes = int(remaining_seconds) // 60
        seconds = remaining_seconds % 60

        if self.seconds % 1 == 0:
            # 秒数が整数値の場合、整数で表示
            self.timestamp = "{:02d}:{:02d}:{:02d}".format(hours, minutes, int(seconds))
        else:
            # 秒数が少数値の場合、少数で表示
            self.timestamp = "{:02d}:{:02d}:{:.3f}".format(hours, minutes, seconds)

        return self.timestamp


def test_timestamp_converter():
    # テストケース1: タイムスタンプから秒数への変換
    converter1 = TimestampConverter(timestamp="01:23:45.678")
    assert converter1.from_timestamp_to_seconds() == 5025.678

    # テストケース2: タイムスタンプから秒数への変換（秒数部が整数）
    converter2 = TimestampConverter(timestamp="00:01:30")
    assert converter2.from_timestamp_to_seconds() == 90

    # テストケース3: タイムスタンプから秒数への変換（時間部がない）
    converter3 = TimestampConverter(timestamp="45.678")
    assert converter3.from_timestamp_to_seconds() == 45.678

    # テストケース4: 秒数からタイムスタンプへの変換
    converter4 = TimestampConverter(seconds=12345.678)
    assert converter4.from_seconds_to_timestamp() == "03:25:45.678"

    # テストケース5: 秒数からタイムスタンプへの変換（秒数部が整数）
    converter5 = TimestampConverter(seconds=90)
    assert converter5.from_seconds_to_timestamp() == "00:01:30"

    # # テストケース6: 秒数からタイムスタンプへの変換（小数点以下の桁数が多い）
    # converter6 = TimestampConverter(seconds=12345.67891234)
    # assert converter6.from_seconds_to_timestamp() == "03:25:45.678"

    # テストケース7: タイムスタンプが与えられていない場合のテスト
    converter7 = TimestampConverter()
    assert converter7.from_timestamp_to_seconds() == 0.0

    # テストケース8: 秒数が与えられていない場合のテスト
    converter8 = TimestampConverter()
    assert converter8.from_seconds_to_timestamp() == "00:00:00.000"

    print("All tests pass.")


# テストの実行
test_timestamp_converter()
