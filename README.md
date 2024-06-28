# Web アプリ概要

- [Web アプリ概要](#web-アプリ概要)
  - [プロジェクト概要](#プロジェクト概要)
    - [背景](#背景)
    - [ターゲット](#ターゲット)
    - [競合となるアプリ、先行研究等](#競合となるアプリ先行研究等)
    - [Web アプリで作りたい理由](#web-アプリで作りたい理由)
    - [YouTube を対象にした理由](#youtube-を対象にした理由)
  - [技術スタック・開発環境](#技術スタック開発環境)
    - [バックエンド](#バックエンド)
    - [フロントエンド](#フロントエンド)
    - [データベース](#データベース)
    - [その他技術](#その他技術)
    - [フォルダ構成](#フォルダ構成)
  - [機能一覧](#機能一覧)
    - [チャンネル一覧](#チャンネル一覧)
      - [チャンネル詳細](#チャンネル詳細)
      - [言語指定](#言語指定)
      - [字幕データ更新](#字幕データ更新)
      - [単語検索機能](#単語検索機能)
      - [単語データ計測](#単語データ計測)
      - [動画一覧](#動画一覧)
        - [動画詳細](#動画詳細)
        - [字幕一覧](#字幕一覧)
          - [字幕詳細](#字幕詳細)
          - [学習ステータス登録](#学習ステータス登録)
          - [字幕詳細更新](#字幕詳細更新)
          - [解説生成](#解説生成)
    - [言語学習記録確認画面](#言語学習記録確認画面)
  - [やりたいことと、案はあるができなさそうなこと](#やりたいことと案はあるができなさそうなこと)
  - [その他](#その他)

## プロジェクト概要

### 背景

外国語を学ぶ際、多くの人が興味を持つコンテンツを利用して学習することで、効率的に自然と身に付けることができる。たとえば、多くの韓国人が日本のアニメやボカロといったオタク文化に触れることで勉強せずに日本語を学んでいるように、日本人も海外のオタクコンテンツを通じて外国語を学ぶことができると考えられる。しかし、現状ではそのような学習方法には多くの労力が伴う。特に、音声を聞いてから字幕を整形する作業や、わからない単語や表現を一つひとつ調べる必要があるため、学習の手間が増してしまう。

一方で、インターネットの普及により、特定のコンテンツに関する情報を共有したり、他人が作成した資料を利用したりすることが容易になっている。例えば、音楽の分野では、かつては好きな曲を耳コピして楽譜を作成していたが、現在では他の誰かが作った楽譜を利用できるようになり、その分演奏の練習に集中できる。同様に、言語学習においてもわからないことを調べる作業を全員が行う必要はなく、一度作成された資料を共有することで、学習効率を大幅に向上させることが可能である。
また、言語を学習するとき、音声付きの教科書を使って勉強することが多い。しかし、そういった教科書の音声は、誰か知らない、特に興味のない人の声で録音されていることが多く、モチベーションにつながりにくい。そのため、好きなアイドルやVTuberなどの声で学習できるようにしたい。

このような背景から、好きな YouTube コンテンツを利用して外国語を学ぶ際の労力を軽減し、同じコンテンツが好きな人同士で情報を共有することで、効率的に学習を進められるシステムを開発したいと考えている。このシステムにより、ユーザーは調べる手間を省き、より多くの時間を実際の学習に費やすことができるようになる。

> 日本人でも、K-POPやKドラマが好きな人は韓国語を勉強せずに自然と身に着けている人がいる。
音声を聞いて、字幕を整形するのは時間がかかる。全員がやる必要はない。
昔は好きな曲をギターで弾きたいと思った時、テレビで放送されるのを待ってそれを録音して、その音源から耳コピをして楽譜に書き起こしてその楽譜が正しいかわからない状態でその曲を練習する必要があった。
しかし、現代では、インターネットが普及し、自分で楽譜を用意しなくても、誰かほかに好きな人が楽譜を作ってくれてたり、売っていたりするのでそういう労力がかかる部分が軽減されていて、弾くことを練習することに時間を使える。
言語学習でも同じように、わからないことを調べる、というのは全員がやる必要がないと思っていて、文法について解説を作るのは最初にわからないと思った人が作って、次に利用する人は、そのデータを引き継げる形にしたい。


### ターゲット

- 外国語を勉強している日本人
- 日本語を勉強している外国人

対応予定のメインの言語は韓国語、英語、日本語。他の言語でも可能だが、詳細な処理は言語ごとに異なるため、事前に予期している言語しか対応されていない機能もある（自然言語処理のライブラリが言語ごとに分かれているため）。

### 競合となるアプリ、先行研究等

- **Learning Language with YouTube（LLY）**

  - 学習対象の字幕がある場合、それをもとに翻訳文が機械翻訳されている。
  - 翻訳文に誤りがあることがあり、教科書的な使い方は難しい。
  - 学習言語とネイティブ言語を同時に照らし合わせながら字幕を確認できない。

- **単語検索機能**
  - 登録されているデータからのみ検索可能なものが多い。
  - 自分の好きなチャンネルで検索を行いたい場合に対応できない可能性がある。

### Web アプリで作りたい理由

- **PC で操作しながらコピペ等を用いて利用できる形式**
  - 効率的に学習が可能。

### YouTube を対象にした理由

- **Netflix や Amazon Prime Video、テレビの問題点**

  - 実際に話している言葉と字幕の内容が一致していないことが多い（言葉が省略されていたり同じ意味で違う言葉等）。
  - 学習言語とネイティブ言語を同時に表示して確認することができない（基本的にどちらか一つの字幕しか表示できない）。
  - テレビの場合、外国語を話しているのを聞いて、自分で耳コピした音をネットで検索して調べる必要がある。

- **YouTube の利点**
  - サブスクリプションサービスでは複数人が同時に話す動画が多いが、YouTube では一人で話す動画が多く、リスニング初心者に優しい。
  - 専門用語について学びやすい。例えば、エンジニア関連、イラスト関連、VTuber 関連の用語など、それぞれの専門分野の用語が学べる。
  - YouTube の場合、動画がアップロードされてしばらくすると、自動で文字起こしされるのでテキストとして確認しやすい。
  - 字幕をテキスト形式で取得することができれば簡単にコピーやペーストができ、翻訳するのも容易になる。
  - YouTube では投稿者が多言語で手動字幕を追加していることが多く、自動字幕に誤りがあっても正しい字幕として学習に利用できる。

## 技術スタック・開発環境

### バックエンド

- **言語**: Python
- **フレームワーク**: Django

### フロントエンド

- **言語**: TypeScript
- **スタイルシート**: SCSS
- **フレームワーク**: Vue.js
- **UI フレームワーク**: Bootstrap

### データベース

- **種類**: PostgreSQL

### その他技術

  - **コンテナ管理**: Docker

### フォルダ構成
- [フォルダ構成](tree.txt)
  
## 機能一覧

### チャンネル一覧

#### チャンネル詳細

- チャンネルの詳細を表示

#### 言語指定

- チャンネルのデフォルト言語を指定し、その言語に対して理解できる言語を指定する（例：デフォルト言語が韓国語、自分が理解できる言語が日本語の場合）。

#### 字幕データ更新

- 指定したチャンネルの言語指定された字幕データをダウンロードする。
- 字幕データは自動生成された自動字幕と手作業で作成された手動字幕の両方をダウンロードする。
- デフォルト言語が韓国語、学習言語が日本語の場合、韓国語の自動字幕、韓国語の手動字幕、日本語の手動字幕が対象として字幕の存在チェックを行う。

#### 単語検索機能

- 手動字幕に対して行ごとに部分一致で検索を行う機能。
- 自動字幕に対しては複数単語に分割して一致検索を行う（全探索でループさせているため時間がかかる）。
- 検索結果にはタイムスタンプ付き動画のリンクがあるので、その単語が話されている箇所を動画で確認できる。


> 日本語を学習している外国人にたまに聞かれることで、「How are you?」って日本語でなんて言うの？と聞かれることがあり、それに対して「元気ですか？」と教えるのが一般的だと思うが、
実際の日本人の会話の中で「元気ですか？」と使うのは体調が悪そうにしているのを見た時ぐらいで、「元気ですか？」を挨拶的な意味合いで使う文化はないと思う。
なので、直訳するとそういった意味になるが、実際にネイティブが使っているのかを確かめるためにもこの単語検索機能は役立つと思う。


#### 単語データ計測

- 手動字幕に対しては空白ごとに文章を分割し、最小の単語数、最小の文字数などを指定し、ランキングを棒グラフで生成する。
- 自動字幕に対しては元々分割されているトークンごとに計測を行う。
- NLTK 等のライブラリを使用しストップワードを除外する。
- レンマ化し、単語の基本形で計測する。


> 外国語を勉強する際に、単語帳に載っている単語を上から学習するのもいいが、単語帳に載っている単語は案外実際の配信では使われないことが多い。
実際に話している字幕データから頻出単語を絞り込むことで、重要な単語を確認できる。
ストップワードを除去しないと、toやtheといった重要でない単語であふれてしまうため計測から除外する。
また、単語の基本形で計測しないと動詞の基本形や過去形なども違う単語として計測されてしまうため基本形にして計測を行う。


#### 動画一覧

- 言語ごとに手動字幕が追加されているかで絞り込みを行うことができる。

##### 動画詳細

- デフォルトの字幕と翻訳言語の字幕を照らし合わせ、字幕の開始時間のタイムスタンプが一致している場合に合わせて登録する。
  タイムスタンプが一致しない場合、前後で取れそうな字幕がないかを確認する。

> 自動字幕だと文字起こしの精度が完ぺきではなく、文章の区切り位置も不自然なためそのままの使用は不可能。使えるようにするためには手作業で文章の区切り位置を修正したり誤字を修正したりする必要がある。（一応spaCy等のnlpのライブラリを使えばある程度読みやすい文章の区切り位置に修正はできる。）しかし、わざわざ手作業で修正するくらいならすでに整形されている手動字幕だけを対象にしたほうが効率が良い。

##### 字幕一覧

- 登録されている字幕データを翻訳字幕と合わせてタイムスタンプ順に表示する。

> 手動字幕でもネイティブ言語と翻訳言語のタイムスタンプで完全に一致していない場合があり、そういったデータはタイムスタンプを完全一致ではなく前のタイムスタンプから後ろのタイムスタンプの間にある字幕、など取得方法を調整している。


###### 字幕詳細

- 学習ステータス、タイムスタンプ付き動画リンク、字幕、翻訳字幕、直訳、翻訳詳細が表示される。
- タイムスタンプ付き動画リンクでその箇所を動画で確認することができる。

###### 学習ステータス登録

- 学習ステータスを登録することができる（未確認、確認したが未学習、一部わからない、学習済み）。

###### 字幕詳細更新

- 字幕と翻訳が登録されており、それに合わせて直訳と翻訳の詳細を登録することができる。

###### 解説生成

- 翻訳の詳細には ChatGPT を用いて形態素解析など文法的な説明を含めた結果を取得することができる。
- ChatGPT の API は無制限ではないので、プロンプトをコピーするボタンを用意している。ブラウザで ChatGPT を開き、そのプロンプトを貼り付けることで同じ結果を得ることができる。
- 結果はコードブロックに出力してもらうようにコピペ用のプロンプトには追加している。
- プロンプト一例
  - [韓国語→日本語](django-project/myproject/resource/chatgpt_translation_prompt/from_ko_to_ja.txt)
  - [英語→日本語](django-project/myproject/resource/chatgpt_translation_prompt/from_en_to_ja.txt)
  
### 言語学習記録確認画面

- 学習ステータスが割り当てられている字幕の履歴を確認することができる。
- 学習言語と学習ステータスで絞り込みができ、一部だけわからないものを再度確認し、理解したらステータスを変えることでわからないものを減らしていくことができる。

## やりたいことと、案はあるができなさそうなこと

- 字幕とタイムスタンプを照らし合わせる人、字幕を付ける人、翻訳をする人、それぞれにポイントを付与し、特定のページに対する権限を与えたい。
- TOPIK, TOEIC, JLPT などの能力試験のレベルごとの単語帳データを学習させ、それに対するチャンネルごとの頻出単語のランキングを作りたい（著作物のため私的利用の範囲でしかできない）。

## その他

- http://localhost:13000/

- `generate_sample_env.py`  
   Git で管理されていない環境ファイルのパラメータサンプルを生成する。

- `tree.py`  
   フォルダ構成を最新化する。
