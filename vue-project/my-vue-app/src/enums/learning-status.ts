enum LearningStatus {
    NOT_CHECKED = 0, // まだ内容を確認していない
    NOT_UNDERSTOOD = 1, // 内容を確認したが理解できていない
    ONE_WORD_UNKNOWN = 2, // 一つだけ単語がわからない
    FULLY_UNDERSTOOD = 3 // すべて理解している
}

const LearningStatusLabel: { name: string; value: number }[] = [
    { name: 'まだ内容を確認していない', value: LearningStatus.NOT_CHECKED },
    { name: '内容を確認したが理解できていない', value: LearningStatus.NOT_UNDERSTOOD },
    { name: '一つだけ単語がわからない', value: LearningStatus.ONE_WORD_UNKNOWN },
    { name: 'すべて理解している', value: LearningStatus.FULLY_UNDERSTOOD }
];


export { LearningStatus, LearningStatusLabel };
