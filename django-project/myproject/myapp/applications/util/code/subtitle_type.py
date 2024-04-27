import unittest
from enum import Enum


class SubtitleType(Enum):
    AUTOMATIC = 0
    MANUAL = 1

    def to_string(self):
        if self == SubtitleType.AUTOMATIC:
            return "automatic_captions"
        elif self == SubtitleType.MANUAL:
            return "subtitles"


class TestSubtitleType(unittest.TestCase):
    def test_to_string(self):
        auto_string = SubtitleType.AUTOMATIC.to_string()
        self.assertEqual(auto_string, "automatic_captions")

        manual_string = SubtitleType.MANUAL.to_string()
        self.assertEqual(manual_string, "subtitles")

    def test_set_from_integer(self):
        auto_from_int = SubtitleType(0)
        self.assertEqual(auto_from_int, SubtitleType.AUTOMATIC)

        manual_from_int = SubtitleType(1)
        self.assertEqual(manual_from_int, SubtitleType.MANUAL)


if __name__ == "__main__":
    unittest.main()
