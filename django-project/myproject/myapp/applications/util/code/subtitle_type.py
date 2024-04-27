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


if __name__ == "__main__":
    unittest.main()
