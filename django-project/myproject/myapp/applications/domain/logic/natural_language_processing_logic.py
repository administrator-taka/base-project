import collections
import logging
import re

import nltk
import spacy
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet

from myapp.applications.util.code.youtube_language import YouTubeLanguage


class NaturalLanguageProcessingLogic:
    def __init__(self):
        # 必要なNLTKデータセットをダウンロード
        nltk.download('stopwords')  # ストップワードのデータセットをダウンロード
        nltk.download('wordnet')  # WordNetのデータセットをダウンロード
        nltk.download('averaged_perceptron_tagger')  # POSタガーのデータセットをダウンロード
        self.lemmatizer = WordNetLemmatizer()  # WordNetのLemmatizerをインスタンス化

        # Spacyの英語モデルをロード(Dockerfileにも記載)
        self.nlp = spacy.load('en_core_web_sm')

    # 指定された言語に応じてストップワードのセットを取得する
    def get_stop_words(self, default_audio_language):
        if default_audio_language == YouTubeLanguage.ENGLISH:
            # NLTKのストップワード
            nltk_stopwords = set(stopwords.words('english'))
            # Spacyのストップワード
            spacy_stopwords = self.nlp.Defaults.stop_words
            # 両方のストップワードを結合
            return nltk_stopwords.union(spacy_stopwords)
        elif default_audio_language == YouTubeLanguage.JAPANESE:
            return {'の', 'に', 'は', 'を', 'た', 'が', 'で', 'て', 'と', 'し', 'れ', 'さ', 'ある', 'いる', 'も', 'する', 'から', 'な',
                    'こと', 'として', 'い', 'や', 'れる', 'など', 'なっ', 'なり', 'いっ', 'その', 'これ', 'それ', 'あれ', 'あの', 'この', 'そう',
                    'いう', 'たち', 'どこ', 'なん', 'でき', 'なかっ', 'どんな', 'いつ', 'もの', 'という'}
        elif default_audio_language == YouTubeLanguage.KOREAN:
            return {'의', '가', '이', '은', '들', '는', '과', '를', '으로', '자', '에', '와', '한', '하다', '그', '도', '수', '등', '에',
                    '와', '의', '이', '가', '로', '에', '과', '를', '을', '으로', '를', '으로', '그리고', '그러나', '또', '하지만', '또한',
                    '그리고'}
        else:
            logging.warning(f"ストップワードリストが見つかりません: {default_audio_language}")
            return set()

    # 単語が有効かどうかをチェックする
    def is_valid_word(self, word, min_word_length, stop_words):
        # 単語の長さが最小長さ以上であることを確認
        is_longer_than_min_length = len(word) >= min_word_length
        # 単語が記号のみで構成されていないことを確認
        is_not_symbol_only = not re.match(r'^[^\w\s]+$', word)
        # 単語が記号で囲まれていないことを確認
        is_not_enclosed_in_symbols = not re.match(r'^\W.*\W$', word)
        # 単語がストップワードリストに含まれていないことを確認
        is_not_stop_word = word.lower() not in stop_words
        # すべての条件を満たす場合にTrueを返す
        return is_longer_than_min_length and is_not_symbol_only and is_not_enclosed_in_symbols and is_not_stop_word

    # 単語リストをフィルタリングする
    def filter_words(self, all_words, min_word_length, stop_words):
        # 有効な単語のみをリストに含める
        return [word for word in all_words if self.is_valid_word(word, min_word_length, stop_words)]

    # フィルタリングされた単語の頻度を計算する
    def calculate_word_frequencies(self, filtered_words, top_n):
        word_counter = collections.Counter(filtered_words)
        # 頻度の高い単語トップNを取得
        top_words = word_counter.most_common(top_n)

        top_words_list = []
        rank = 1
        prev_count = None
        prev_rank = 1
        # 同率の場合の順位を考慮してリストに単語とその頻度を追加
        for word, count in top_words:
            if count != prev_count:
                prev_rank = rank
            rank += 1
            top_words_list.append({"rank": prev_rank, "word": word, "count": count})
            prev_count = count

        return top_words_list

    # 単語リストから指定された数の連続した単語の組み合わせを作成する
    def get_combinations(self, words, min_word):
        combinations = []
        # 指定された最小単語数に基づいて組み合わせを作成
        for i in range(len(words) - min_word + 1):
            combination = ' '.join(words[i:i + min_word])
            combinations.append(combination)
        return combinations

    # 単語の品詞タグを取得
    def lemmatize_word(self, word):
        pos_tag = nltk.pos_tag([word])[0][1][0].lower()  # 単語の品詞タグを取得し、小文字に変換
        wordnet_pos = self.get_wordnet_pos(pos_tag)  # NLTKの品詞タグをWordNetの品詞タグに変換

        # 単語をレンマ化（基本形に変換）
        if wordnet_pos:
            return self.lemmatizer.lemmatize(word, wordnet_pos)  # WordNetを使って単語を基本形に変換
        else:
            return self.lemmatizer.lemmatize(word)  # 特定の品詞タグがない場合は、通常の方法で基本形に変換

    # NLTKの品詞タグをWordNetの品詞タグに変換
    def get_wordnet_pos(self, pos_tag):
        if pos_tag.startswith('j'):  # 形容詞
            return wordnet.ADJ
        elif pos_tag.startswith('v'):  # 動詞
            return wordnet.VERB
        elif pos_tag.startswith('n'):  # 名詞
            return wordnet.NOUN
        elif pos_tag.startswith('r'):  # 副詞
            return wordnet.ADV
        else:
            return None  # 未知の品詞タグの場合はNoneを返す
