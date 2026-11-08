# 日本語入力とフォーム

版: 1.0.1。資料確認日: 2026-11-08。

catalog.jsonから生成。数値の目安と公開実践は、用途に合わせて比較する。

## F01 変換確定Enterで送信しない

根拠の種類: 技術仕様・標準の解説。対象: 日本語。

使う場面: Enterキーに独自の検索・送信・決定処理を割り当てるとき。

独自のEnter送信ではIME変換中かを判定する。isComposingだけで対象のSafariまで保証したとしない。ボタンからの送信も残す。

例: 変換候補の確定をEnterで行い、その後の明示的な送信を区別する。

例外・注意: 対象環境によって229判定等の補助が必要になる。固定時間の待機で全IMEを保証しない。

確認: 実OS・IMEで変換中、確定直後、通常Enter、Shift+Enter、送信ボタンを確認する。

出典: [Google Chrome IME-safe enter-to-submit](https://developer.chrome.com/docs/modern-web-guidance/guides/forms/ime-safe-enter-submit)

## F02 入力中の値を勝手に整形しない

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語。

使う場面: 日本語の入力欄や、氏名・住所など日本語を含むデータを扱うフォームを実装するとき。

未確定文字を毎キーで置き換えない。整形が必要なら、確定後の時点と対象フィールドを決め、元の値を損なわないようにする。

例: かな変換の途中で全角数字を半角へ書き換えない。

例外・注意: 検索補助と登録する氏名では許容できる変換が異なる。仕様があれば優先する。

確認: 候補選択、カーソル移動、貼り付け、取り消しを実際に操作する。

出典: [Google Chrome IME-safe enter-to-submit](https://developer.chrome.com/docs/modern-web-guidance/guides/forms/ime-safe-enter-submit)、[Unicode UAX #15](https://www.unicode.org/reports/tr15/)

## F03 氏名の構造を決めつけない

根拠の種類: 公開実践（適用範囲を確認する）。対象: 日本語で差が出やすい共通事項。

使う場面: 日本語の入力欄や、氏名・住所など日本語を含むデータを扱うフォームを実装するとき。

業務で姓と名の区別が必要かを確認する。必要な場合もラベルと順序を明示し、外国籍の利用者や単名を想定する。

例: 「氏名」一欄と、「姓」「名」の二欄をデータ利用目的から選ぶ。

例外・注意: 本人確認等で構造が指定されている場合は、例外時の案内も用意する。

確認: 長い名前、中黒、空白、単名、漢字以外を含む名前で確認する。

出典: [W3C Personal names around the world](https://www.w3.org/International/questions/qa-personal-names)

## F04 ふりがなと文字種の制約を目的から決める

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語。

使う場面: 日本語の入力欄や、氏名・住所など日本語を含むデータを扱うフォームを実装するとき。

読み仮名を収集する理由を確認し、必要な文字種と例を入力前に示す。見た目だけで全角やカタカナを強制しない。

例: 「フリガナ」の説明に、受け付ける表記と必要な理由を添える。

例外・注意: 外部システムの制約がある場合は、その範囲と修正方法を案内する。

確認: ひらがな、カタカナ、長音、中黒、空白で期待する受理・案内になるか確認する。

出典: [W3C Personal names around the world](https://www.w3.org/International/questions/qa-personal-names)、[デジタル庁 インプットテキスト: 使い方](https://design.digital.go.jp/dads/components/input-text/usage/)

## F05 住所の自動入力後も修正できるようにする

根拠の種類: 編集上の仮説（実画面で比較する）。対象: 日本語。

使う場面: 日本語の入力欄や、氏名・住所など日本語を含むデータを扱うフォームを実装するとき。

日本の住所を扱う場合は郵便番号補助を検討し、補完失敗や新しい住所でも手動入力できる経路を残す。

例: 郵便番号から都道府県等を補完しても、町名や建物名を編集できるようにする。

例外・注意: 日本語サイトが国内住所だけを受け付けるとは限らない。対象地域を先に決める。

確認: ハイフンあり・なし、補完0件、集合住宅、長い住所、対象外国住所を確認する。

出典: [デジタル庁 インプットテキスト: 使い方](https://design.digital.go.jp/dads/components/input-text/usage/)、[WHATWG HTML autofill](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill)

## F06 桁のある識別子を数値にしない

根拠の種類: 技術仕様・標準の解説。対象: 日本語で差が出やすい共通事項。

使う場面: 日本語の入力欄や、氏名・住所など日本語を含むデータを扱うフォームを実装するとき。

郵便番号や電話番号など計算しない文字列を、先頭の0を落とす数値モデルにしない。typeとinputmodeを目的に合わせて選ぶ。

例: 郵便番号はtextとnumeric入力補助、電話番号はtelを候補にする。

例外・注意: 国際番号、内線、記号の有無は実際の対象範囲で決める。

確認: 先頭0、貼り付け、戻る操作、自動入力で値が変わらないか確認する。

出典: [WHATWG HTML autofill](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill)、[デジタル庁 インプットテキスト: 使い方](https://design.digital.go.jp/dads/components/input-text/usage/)

## F07 説明とエラーを入力中も見せる

根拠の種類: 公開実践（適用範囲を確認する）。対象: 日本語で差が出やすい共通事項。

使う場面: 日本語の入力欄や、氏名・住所など日本語を含むデータを扱うフォームを実装するとき。

labelを置き、必要な条件と例をサポートテキストにする。placeholderだけに説明を置かず、必須・任意を文字でも示す。

例: 「郵便番号」の下に入力例を表示し、エラーと区別する。

例外・注意: デジタル庁の記号の使い方は、そのデザインシステムのルールであり全製品への義務ではない。

確認: 入力済み、エラー、読み上げの各状態で、条件と対象を特定できるか確認する。

出典: [デジタル庁 インプットテキスト: 使い方](https://design.digital.go.jp/dads/components/input-text/usage/)、[デジタル庁 インプットテキスト: アクセシビリティ](https://design.digital.go.jp/dads/components/input-text/accessibility/)

## F08 文字数制限を変換中に衝突させない

根拠の種類: 公開実践（適用範囲を確認する）。対象: 日本語。

使う場面: 文字数上限のある入力欄で、変換途中や貼り付けを制限するとき。

maxlengthで変換前のかなや貼り付けを切り捨てないか確認する。長さの単位と検証時点を定め、超過時には上限と修正方法を示す。

例: 「が」、結合濁点、絵文字を、仕様で定めた文字数として数える。

例外・注意: UTF-16長、書記素数、バイト数のどれが正しいかは保存先の契約で異なる。

確認: 上限前後、長いかなからの漢字変換、貼り付け、送信後の入力保持を確認する。

出典: [デジタル庁 インプットテキスト: アクセシビリティ](https://design.digital.go.jp/dads/components/input-text/accessibility/)、[Mozilla Intl.Segmenter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter)
