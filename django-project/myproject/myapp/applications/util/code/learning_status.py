from enum import Enum


class LearningStatus(Enum):
    NOT_CHECKED = 0  # まだ内容を確認していない
    NOT_UNDERSTOOD = 1  # 内容を確認したが理解できていない
    ONE_WORD_UNKNOWN = 2  # 一つだけ単語がわからない
    FULLY_UNDERSTOOD = 3  # すべて理解している
