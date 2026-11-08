# 参照資料と限界

資料確認日: 2026-11-08。原文の転載ではなく、自作の説明から参照する。

## jlreq

[W3C 日本語組版処理の要件](https://www.w3.org/TR/jlreq/)

組版要件を説明するWorking Group Note。Webの一律の適合基準ではない。

## css-text3

[W3C CSS Text Level 3](https://www.w3.org/TR/css-text-3/)

改行・禁則・均等配置の定義。実装状況は別途確認する。

## css-text4

[W3C CSS Text Level 4](https://www.w3.org/TR/css-text-4/)

作業草案。新しい組版機能を全ブラウザの既定動作とみなさない。

## css-values

[W3C CSS Values: ic](https://www.w3.org/TR/css-values-4/#ic)

icは基準文字の送り幅に基づく単位。実際の全文章の文字数とは異なる。

## dads-type

[デジタル庁 タイポグラフィ](https://design.digital.go.jp/dads/foundations/typography/)

行政サービスの基準。数値を全サイトへの義務へ拡張しない。

## smarthr-type

[SmartHR デザイントークン: タイポグラフィ](https://smarthr.design/products/design-tokens/typography/)

業務UIでの書体・サイズ・行送り・表の実例。

## smarthr-webfont

[SmartHR ウェブサイトのタイポグラフィ](https://smarthr.design/basics/typography/website/)

游ゴシックのOS別ウェイト差。利用環境で再確認する。

## smarthr-font

[SmartHR 基本要素: タイポグラフィ](https://smarthr.design/basics/typography/)

用途とフォントの性能・利用環境を併せて選ぶ事例。

## html-lang

[W3C Declaring language in HTML](https://www.w3.org/International/questions/qa-html-language-declarations)

言語指定の解説。フォントを固定する機能ではない。

## font-performance

[Google web.dev Best practices for fonts](https://web.dev/articles/font-best-practices)

フォント配信とレイアウト移動。日本語に限定した資料ではない。

## font-features

[Mozilla font-feature-settings](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-feature-settings)

OpenType低水準指定。利用フォントに依存する。

## east-asian

[Mozilla font-variant-east-asian](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-east-asian)

pwidとpaltを同じ機能として扱わない。

## autospace

[Mozilla text-autospace](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-autospace)

自動の和欧間隔。構文の受理と実際の組版品質は別。

## spacing-trim

[Mozilla text-spacing-trim](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-spacing-trim)

句読点等の空きの調整。対応状況を対象環境で確認する。

## word-break

[Mozilla word-break](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/word-break)

keep-all、normal、auto-phraseの相違。

## ruby

[WHATWG HTML ruby](https://html.spec.whatwg.org/multipage/text-level-semantics.html#the-ruby-element)

現行HTMLのrubyとrt。過去のXHTML Ruby仕様を実装手順に使わない。

## writing-mode

[Mozilla writing-mode](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/writing-mode)

縦組みの機能。縦書きを推奨する美的根拠ではない。

## dads-spacing

[デジタル庁 余白](https://design.digital.go.jp/dads/foundations/spacing/)

余白と情報のまとまりを扱う公開実践。

## dads-layout

[デジタル庁 レイアウト](https://design.digital.go.jp/dads/foundations/layout/)

情報構造・グリッド・表示幅の公開実践。

## smarthr-button

[SmartHR Button](https://smarthr.design/products/components/button/)

ボタンラベル、優先順位、状態の公開実践。

## smarthr-writing

[SmartHR その他のUIテキスト](https://smarthr.design/products/contents/ui-text/app-writing/)

日本語UIの文言の公開実践。企業の文体をそのまま強制しない。

## smarthr-error

[SmartHR エラーメッセージ](https://smarthr.design/products/contents/error-messages/)

エラーの原因と次にできる操作を伝える公開実践。

## dads-input

[デジタル庁 インプットテキスト: 使い方](https://design.digital.go.jp/dads/components/input-text/usage/)

ラベル、補足、入力幅、エラー表示の公開実践。

## dads-input-a11y

[デジタル庁 インプットテキスト: アクセシビリティ](https://design.digital.go.jp/dads/components/input-text/accessibility/)

入力中に消える説明、最大長、コピーの制限等を扱う。

## names

[W3C Personal names around the world](https://www.w3.org/International/questions/qa-personal-names)

姓名の構造を一律に仮定しないための解説。

## unicode-normalization

[Unicode UAX #15](https://www.unicode.org/reports/tr15/)

正規化の仕様。検索用途と原文保存の方針は製品側で決める。

## ime

[Google Chrome IME-safe enter-to-submit](https://developer.chrome.com/docs/modern-web-guidance/guides/forms/ime-safe-enter-submit)

変換確定Enterと送信の衝突。実OS・IMEでの確認を残す。

## autofill

[WHATWG HTML autofill](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill)

autocompleteの意味とトークン。データモデルの決定までは代行しない。

## number-format

[Mozilla Intl.NumberFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat)

通貨・数値の表示。税や契約条件を決めるAPIではない。

## date-format

[Mozilla Intl.DateTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat)

暦・日時・タイムゾーンを明示するAPI。

## segmenter

[Mozilla Intl.Segmenter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter)

書記素・語等の分割。最大長の業務上の定義は別途必要。

## text-spacing

[W3C WCAG 2.2 Understanding: Text Spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html)

既定値を指定する義務ではなく、利用者による変更への耐性。

## reflow

[W3C WCAG 2.2 Understanding: Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)

320 CSS px相当のリフロー。二次元表などの例外を含む。

## contrast

[W3C WCAG 2.2 Understanding: Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

文字コントラストの解説。サイズ・太さ・例外を確認する。

## text-images

[W3C WCAG 2.2 Understanding: Images of Text](https://www.w3.org/WAI/WCAG22/Understanding/images-of-text.html)

文字画像の扱い。ロゴ等の例外を含む。

## target-size

[W3C WCAG 2.2 Understanding: Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

AAは24 CSS px基準と例外。44 CSS pxをAAの一律基準としない。

## language

[W3C WCAG 2.2 Understanding: Language of Page](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html)

文書言語と読み上げ・表示。

## utf8

[W3C Multilingual form encoding](https://www.w3.org/International/questions/qa-forms-utf-8)

日本語を含むフォームのエンコーディング。

## link-text

[デジタル庁 リンクテキスト: アクセシビリティ](https://design.digital.go.jp/dads/foundations/link-text/accessibility/)

リンク先が区別できる文言とアクセシブルな名前。
