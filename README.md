# 日本語Webデザイン補助

いつものデザインスキルに、日本語の調整を。

和欧混植、見出しの改行、文字の密度、UI文言、日本語入力を扱うAgent Skillです。frontend-designなどの既存スキルと併用し、ブランドや構成を保ちながら日本語の実文で調整します。

[Webガイド](https://japanese-design.sakimyto.com/) · [AI向け資料](https://japanese-design.sakimyto.com/for-ai/) · [v1.0.1のZIP](https://github.com/sakimyto/japanese-web-design/releases/tag/v1.0.1) · [sakimytoの実験](https://sakimyto.com/lab/japanese-web-design)

## 導入

[skills CLI](https://github.com/vercel-labs/skills)で、プロジェクトのディレクトリから追加します。Node.jsの条件はCLIの公式資料で確認してください。

```sh
npx skills add https://github.com/sakimyto/japanese-web-design/tree/v1.0.1/skills/japanese-web-design --skill japanese-web-design
```

導入するエージェントを選びます。Codexへ指定する場合は `--agent codex`、Claude Codeへ指定する場合は `--agent claude-code` を付けられます。同名のスキルがある場合は、更新前に内容を確認してください。グローバル導入は必要なときだけ選びます。

ZIPを使う場合は、展開した `japanese-web-design/` フォルダ全体をエージェントのスキル探索先へ配置します。Codexのプロジェクト設定なら `.agents/skills/japanese-web-design/` です。探索先やZIPアップロードへの対応は製品ごとに異なります。

## 既存のデザインスキルと使う

```text
frontend-design と japanese-web-design を使って、日本語の料金ページを作って。
既存のブランド方針を保ち、見出しの改行、文字の密度、価格と条件のまとまり、
操作ラベルを調整して。適用したルールと、未確認の表示・動作も教えて。
```

レビューにも使えます。

```text
japanese-web-design を使って、この画面の日本語をレビューして。
まず実文の改行と和欧混植を確認し、入力欄があればIMEと文字数制限も見て。
指摘にはルールID、観測した問題、修正案、確認方法を付けて。
```

スキル同士を自動で順番に起動する機能はありません。併用を依頼すると、補助スキルが必要な分野の資料を参照します。既存のデザインシステムを上書きするCSS、必須のネット接続、実行スクリプト、フォント本体はスキルへ含めていません。

## 収録内容

一次資料39件を参照した8分野64項目。各項目に、使う場面、実践、例、例外、確認方法、出典があります。

| 分野 | 主な内容 |
| --- | --- |
| [書体と文字の密度](skills/japanese-web-design/references/typography.md) | 日本語の実グリフ、OS差、行高・字間、和欧混植、フォント配信 |
| [改行と日本語組版](skills/japanese-web-design/references/composition.md) | 禁則、keep-all、固定改行、palt、約物、ルビ、縦組み |
| [情報のまとまり](skills/japanese-web-design/references/layout.md) | 日本語見出し、行長、余白、密度、カード、ボタン |
| [UI文言](skills/japanese-web-design/references/writing.md) | 操作語、状態、敬語、エラー、リンク、コピーの意味 |
| [日本語入力](skills/japanese-web-design/references/forms.md) | IME、氏名、ふりがな、住所、先頭0、最大長 |
| [表記とデータ](skills/japanese-web-design/references/locale.md) | Unicode正規化、通貨、万・億、日時、和暦、桁揃え |
| [アクセシビリティ](skills/japanese-web-design/references/accessibility.md) | 拡大、字間変更、文字画像、読み上げ、ターゲット領域 |
| [評価](skills/japanese-web-design/references/review.md) | 実文、比較条件、境界幅、例外、効果の主張 |

[実装例](skills/japanese-web-design/references/recipes.md)と[8つの評価課題](skills/japanese-web-design/references/evaluation.md)も同梱します。

技術仕様・標準の解説は18項目、企業等の公開実践は13項目、編集上の仮説は33項目。特定企業のサイズ基準や数値の目安を、全ての日本語サイトの義務にはしません。日本語固有の判断に加え、日本語で問題が出やすい共通事項も含みます。

## 検証と限界

データ・出典の整合、生成資料との一致、ZIPの内容、検索条件の組合せ、不正な文字列を使ったHTMLの検査を行います。公開ページはJavaScriptを無効にしても全項目を読める構造です。

生成AIの出力改善率や、日本語話者による独立した比較評価はまだ測定していません。Webガイドの修正例は自作の編集例であり、スキルの効果を測った実験結果ではありません。実IMEやスクリーンリーダーを含む全環境への対応も保証しません。確認した範囲は [検証記録](docs/verification.md) に残します。

## 開発

Python 3.15.0とNode.js 26.12.1で検査しています。生成とテストに追加のライブラリは不要です。

```sh
bun run build
bun run test
```

編集元は `catalog.json`。ルールを変えたら、生成した参照Markdownと同じ変更に含めます。Webガイドも同じデータから生成します。CSS例・実装例・評価課題・スキル本体はそれぞれの元ファイルを編集します。

サイトのローカル表示は `bun run dev`。公開手順と復旧方法は [releasing.md](docs/releasing.md) にあります。

## ライセンスと出典

自作部分は[MIT](LICENSE)。第三者の資料はリンクで参照し、ライセンスを変更したり、本文・フォント・画像を再配布したりしません。[参照資料と限界](skills/japanese-web-design/references/sources.md)に各資料の役割を記録しています。

## English quick start

An additive Agent Skill for Japanese web typography and UI. Use it alongside your preferred design skill; it preserves the project's visual direction and adds Japanese-content checks. The reference material is in Japanese.

Install with the command above, then ask: “Use frontend-design and japanese-web-design to build this Japanese page. Preserve the brand direction and review real Japanese copy, line breaks, mixed Latin/Japanese type, density, and form input.”

The 64 rules distinguish technical specifications, published practices, and editorial hypotheses. This project does not claim a measured improvement in generated designs or conversion rates.
