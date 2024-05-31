enum YouTubeLanguage {
    JAPANESE = "ja",  // 日本語
    ENGLISH = "en",   // 英語
    KOREAN = "ko",    // 韓国語
    CHINESE = "zh",   // 中国語
    INDONESIAN = "id",  // インドネシア語
    NEPALI = "ne",  // ネパール語
    // 以下、未確認の言語
    AFRIKAANS = "af",
    AMHARIC = "am",
    ARABIC = "ar",
    // 他の言語も同様に追加
    ZULU = "zu"
}

const YouTubeLanguageLabel: { name: string; value: string }[] = [
    { name: '日本語', value: YouTubeLanguage.JAPANESE },
    { name: '英語', value: YouTubeLanguage.ENGLISH },
    { name: '韓国語', value: YouTubeLanguage.KOREAN },
    { name: '中国語', value: YouTubeLanguage.CHINESE },
    { name: 'インドネシア語', value: YouTubeLanguage.INDONESIAN },
    { name: 'ネパール語', value: YouTubeLanguage.NEPALI },
    // 以下、未確認の言語
    { name: 'アフリカーンス語', value: YouTubeLanguage.AFRIKAANS },
    { name: 'アムハラ語', value: YouTubeLanguage.AMHARIC },
    { name: 'アラビア語', value: YouTubeLanguage.ARABIC },
    // 他の言語も同様に追加
    { name: 'ズールー語', value: YouTubeLanguage.ZULU }
];

const getYouTubeLanguagesFromCodes = (codes: string[]): { name: string; value: string }[] =>
    codes.map(code => {
        const language = YouTubeLanguageLabel.find(lang => lang.value === code);
        return language ? language : { name: '', value: '' };
    });


    export { YouTubeLanguage, YouTubeLanguageLabel, getYouTubeLanguagesFromCodes };
