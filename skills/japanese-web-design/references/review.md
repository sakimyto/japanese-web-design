# こなれ感を評価するための確認

版: 1.0.1。資料確認日: 2026-11-08。

catalog.jsonから生成。数値の目安と公開実践は、用途に合わせて比較する。

## R01 実文で判断する

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語で差が出やすい共通事項。

使う場面: 日本語UIの修正案、追加スキルの効果、公開する主張を比較するとき。

最終評価には日本語の実文か、同じ長さ・役割の例文を使う。Lorem ipsumの画面だけで日本語の完成度を判定しない。

例: 漢字、かな、英語、数字、括弧を含む見出しと段落を入れる。

例外・注意: 未確定コピーは未確定と記録する。架空の実績や価格を本番データのように出さない。

確認: コピーが変わると崩れそうな部分を、長い例文で再確認する。

出典: [デジタル庁 レイアウト](https://design.digital.go.jp/dads/foundations/layout/)、[デジタル庁 タイポグラフィ](https://design.digital.go.jp/dads/foundations/typography/)

## R02 複数の画面の役割で比較する

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語で差が出やすい共通事項。

使う場面: 日本語UIの修正案、追加スキルの効果、公開する主張を比較するとき。

SaaSの紹介、長文記事、業務UI等を別の課題として評価する。一つの見た目を全用途へ広げない。

例: 料金表と読み物と入力フォームで、密度と改行の採点を分ける。

例外・注意: 今回扱わない用途へ効果を外挿しない。

確認: 各課題の内容理解と操作に必要な情報を確認する。

出典: [デジタル庁 レイアウト](https://design.digital.go.jp/dads/foundations/layout/)、[SmartHR デザイントークン: タイポグラフィ](https://smarthr.design/products/design-tokens/typography/)

## R03 比較条件を固定する

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語で差が出やすい共通事項。

使う場面: 日本語UIの修正案、追加スキルの効果、公開する主張を比較するとき。

ベースのデザインスキル、モデル、入力文、画面幅、フォントを固定し、追加スキルの有無で比較する。

例: 同じ課題・同じ文章で作った二案を並べる。

例外・注意: 生成のゆらぎがあるため、一つの成功例から平均の改善率を主張しない。

確認: 条件・差分・失敗例を保存し、変更した条件を明記する。

出典: [デジタル庁 レイアウト](https://design.digital.go.jp/dads/foundations/layout/)、[Google web.dev Best practices for fonts](https://web.dev/articles/font-best-practices)

## R04 美的な評価と操作の失敗を分ける

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語で差が出やすい共通事項。

使う場面: 日本語UIの修正案、追加スキルの効果、公開する主張を比較するとき。

読めない、操作できない、入力が失われる問題を先に解消する。字間や印象の好みは別の評価軸で比較する。

例: IME誤送信を直したうえで、見出しの印象を評価する。

例外・注意: 見た目の評点を、全規格への適合やCVR向上の証明に読み替えない。

確認: 障害と好みの指摘を分け、再現条件を記録する。

出典: [W3C WCAG 2.2 Understanding: Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)、[Google Chrome IME-safe enter-to-submit](https://developer.chrome.com/docs/modern-web-guidance/guides/forms/ime-safe-enter-submit)

## R05 狭い幅と長い文言を掛け合わせる

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語。

使う場面: 日本語UIの修正案、追加スキルの効果、公開する主張を比較するとき。

通常文だけでなく、最長の想定名称、注記、エラー、数値を狭い幅へ入れる。例外処理は内容を隠す前に見直す。

例: 長い会社名、40文字の見出し、複数行のエラーを同じ画面に置く。

例外・注意: 長さの上限が仕様にあれば、その前後を使う。無限長への保証は主張しない。

確認: 代表幅に加えて境界の幅で、欠落・重なり・操作不能を記録する。

出典: [W3C WCAG 2.2 Understanding: Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)、[Mozilla word-break](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/word-break)

## R06 新しい組版機能は無効時も確認する

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語。

使う場面: 日本語UIの修正案、追加スキルの効果、公開する主張を比較するとき。

auto-phrase、text-autospace、text-spacing-trim等は、CSSの受理と対象ブラウザの表示を確認し、無効でも読める基本スタイルを保つ。

例: @supportsの有無と対象ブラウザで、同じ見出しを比較する。

例外・注意: @supportsが真でも望む字形・改行・フォント機能まで保証しない。

確認: 機能を外した状態、フォントが違う状態を比較する。

出典: [Mozilla text-autospace](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-autospace)、[Mozilla text-spacing-trim](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-spacing-trim)、[Mozilla word-break](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/word-break)

## R07 ルールを適用しない理由を残す

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語で差が出やすい共通事項。

使う場面: 日本語UIの修正案、追加スキルの効果、公開する主張を比較するとき。

特定企業の数値や編集上の目安を、既存ブランド・用途へ無条件に上書きしない。適用する理由と、例外の判断を短く残す。

例: 高密度の管理画面で、記事本文向けの1.8の行高を採用しない理由を示す。

例外・注意: 安全性や必須のアクセシビリティ要件を、好みを理由に無視しない。

確認: ルールIDと、適用・非適用・未確認の理由を照合する。

出典: [デジタル庁 タイポグラフィ](https://design.digital.go.jp/dads/foundations/typography/)、[SmartHR デザイントークン: タイポグラフィ](https://smarthr.design/products/design-tokens/typography/)

## R08 効果を観測できる主張にする

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語で差が出やすい共通事項。

使う場面: 日本語UIの修正案、追加スキルの効果、公開する主張を比較するとき。

「こなれた」だけで終えず、階層、改行、密度、和欧混植、文言の理解、入力の支障を別々に記録する。

例: 日本語話者に二案を順序を隠して見せ、理由と次の操作の理解を聞く。

例外・注意: 利用者試験をしていない段階で、改善率・CVR・滞在時間の増加を創作しない。

確認: 評価者の人数、条件、判定できなかった範囲を記録する。

出典: [デジタル庁 レイアウト](https://design.digital.go.jp/dads/foundations/layout/)、[デジタル庁 リンクテキスト: アクセシビリティ](https://design.digital.go.jp/dads/foundations/link-text/accessibility/)
