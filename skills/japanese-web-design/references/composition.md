# 改行と日本語組版

版: 1.0.0。資料確認日: 2026-11-08。

catalog.jsonから生成。数値の目安と公開実践は、用途に合わせて比較する。

## C01 言語を宣言して禁則を確認する

根拠の種類: 技術仕様・標準の解説。対象: 日本語。

使う場面: 見出しや本文の改行、句読点の位置、和欧混植の間隔を調整するとき。

日本語の文書には適切なlangを宣言する。通常の改行を基点にし、必要な箇所でline-break:strictを比較する。

例: 「『次の一歩』を、今日から。」の句読点と括弧を見る。

例外・注意: strictは全ての見出しの意味的な改行を保証しない。多言語ページ全体をjaにしない。

確認: 「、。）」が行頭に孤立せず、「（」が行末に残らないか対象ブラウザで確認する。

出典: [W3C Declaring language in HTML](https://www.w3.org/International/questions/qa-html-language-declarations)、[W3C CSS Text Level 3](https://www.w3.org/TR/css-text-3/)

## C02 CJKの折り返しを止めない

根拠の種類: 技術仕様・標準の解説。対象: 日本語。

使う場面: 日本語が狭いカードからはみ出す、または欧文の単語が途中で切れるとき。

word-break:normalを基点にし、keep-allを日本語本文全体に設定しない。break-allも英語の長い語を壊すため、全体への設定を避ける。

例: 「お問い合わせはこちらから」を狭いカードへ入れる。

例外・注意: 短い固有名詞を一塊にしたい場合は局所指定と、幅不足の処理を用意する。

確認: 320px相当と長い固有名詞で横にはみ出さないか確かめる。

出典: [Mozilla word-break](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/word-break)

## C03 意味の切れ目と画面幅を両方見る

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語。

使う場面: 助詞や接尾辞だけが最終行に残るなど、意味のまとまりと表示幅が合わないとき。

助詞や接尾辞だけの最終行を避けたい場合は、文言・幅・サイズ・改行候補を比較する。見出し全体のnowrapで解決しない。

例: 「毎日の経理を、もっと軽く。」を一行、二行、三行で読む。

例外・注意: 一字だけの最終行は直ちに規格違反ではない。短歌や固有のコピーは意図を守る。

確認: 各幅で意味を追え、調整のために主張を変えていないか確認する。

出典: [W3C 日本語組版処理の要件](https://www.w3.org/TR/jlreq/)、[Mozilla word-break](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/word-break)

## C04 固定改行は対象のコピーに限定する

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語。

使う場面: 見出しや本文の改行、句読点の位置、和欧混植の間隔を調整するとき。

CMS本文へ表示幅依存のbrを埋め込まず、短いコピーに必要な場合だけ使う。wbrは改行候補であり、日本語の他の改行を禁止しない。

例: PC用の「二行の見出し」をスマホでも同じ改行に固定しない。

例外・注意: 詩、住所の構造、編集上の改行には意味があるため保つ。

確認: 文字を拡大し、brの前後に一字だけの行が出ないか確認する。

出典: [W3C CSS Text Level 3](https://www.w3.org/TR/css-text-3/)、[W3C WCAG 2.2 Understanding: Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)

## C05 均等配置の副作用を見極める

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語。

使う場面: 見出しや本文の改行、句読点の位置、和欧混植の間隔を調整するとき。

短い説明文やカードでは左揃えを基点にし、text-align:justifyによる字間の伸びを確認する。長文の均等配置は目的がある場合に比較する。

例: 数字と英語を含む短い段落で、文字間の空きが大きく変わらないかを見る。

例外・注意: 出版物に近い長文の組版まで一律に禁止しない。

確認: 段落末尾、長い英語、約物の連続を含む実文で比較する。

出典: [W3C CSS Text Level 3](https://www.w3.org/TR/css-text-3/)

## C06 paltと句読点の調整を区別する

根拠の種類: 技術仕様・標準の解説。対象: 日本語。

使う場面: 括弧の余白や見出しの字面を詰めるためにOpenType機能を使うとき。

paltはフォントの字幅・間隔に関わる機能で、pwidとは異なる。句読点の空きを調整する目的ならtext-spacing-trimも比較し、本文全体への重ね掛けを避ける。

例: 短い見出しの括弧だけを検討し、表の桁揃えは保つ。

例外・注意: 対応するOpenType機能がなければ同じ結果にはならない。

確認: 有効・無効の両方で本文、括弧、価格、表の幅を比較する。

出典: [Mozilla font-feature-settings](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-feature-settings)、[Mozilla font-variant-east-asian](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-east-asian)、[Mozilla text-spacing-trim](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-spacing-trim)

## C07 和欧間隔をデータの空白だけで作らない

根拠の種類: 技術仕様・標準の解説。対象: 日本語で差が出やすい共通事項。

使う場面: 見出しや本文の改行、句読点の位置、和欧混植の間隔を調整するとき。

text-autospace等を検討するときは対応環境を確認し、保存する文字列と見た目の間隔を区別する。原文の空白を一括挿入・削除しない。

例: 「AIで作るWebサイト」と「2026年11月」の空きを比較する。

例外・注意: 製品名・コード・利用者入力の空白には意味があり得る。

確認: コピーした値を照合し、機能が無効でも文意が保たれるか確かめる。

出典: [Mozilla text-autospace](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-autospace)、[W3C CSS Text Level 4](https://www.w3.org/TR/css-text-4/)

## C08 ルビと縦組みは専用の確認をする

根拠の種類: 技術仕様・標準の解説。対象: 日本語。

使う場面: 見出しや本文の改行、句読点の位置、和欧混植の間隔を調整するとき。

ルビはruby・rtを使い、縦組みはwriting-mode等で表す。一文字ずつbrを入れて縦書きを模倣しない。

例: 「組版」にルビを付け、縦組みの「2026」「（仮）」を見る。

例外・注意: 横組みの全画面を縦組みに変える義務はない。読み上げ挙動は環境で異なる。

確認: 数字・括弧の向き、ルビの重なり、選択・コピー、読み上げ順を実機で確認する。

出典: [WHATWG HTML ruby](https://html.spec.whatwg.org/multipage/text-level-semantics.html#the-ruby-element)、[Mozilla writing-mode](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/writing-mode)
