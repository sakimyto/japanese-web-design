# 日本語の画面で試す実装例

既存のコンポーネントとデザイントークンを先に確認する。以下は特定の問題を比較するための例であり、画面全体への一括適用はしない。数値は編集上の仮説。対象ブラウザと実フォントで確認する。

## 見出しが窮屈に見える

関係する項目: T04、T05、C02、C03。日本語の複数行見出しでは、英語の短い見出し向けの行高と字間を見直す。

```css
.hero-title:lang(ja) {
  font-size: clamp(2rem, 5vw, 3.5rem);
  line-height: 1.4;
  letter-spacing: normal;
  word-break: normal;
  line-break: strict;
}
```

まず幅と文字サイズで調整する。`white-space: nowrap` を見出し全体へ加えたり、本文へ幅に依存する `br` を大量に埋め込んだりしない。助詞だけの最終行を避ける場合も、コピーの条件や意味を削らない。`word-break: auto-phrase` を比較するときは対象ブラウザと無効時の表示を確認し、短い見出しと長い本文を別に評価する。

## 本文の幅を日本語で検討する

関係する項目: L03、C05。`ic` は基準文字の送り幅から決まる単位で、文章中の文字数そのものではない。`ch` も日本語一文字の幅ではない。

```css
.article-body:lang(ja) {
  max-inline-size: 42rem;
  max-inline-size: 40ic;
  line-height: 1.75;
  letter-spacing: normal;
  text-align: start;
}

.article-body .long-url {
  overflow-wrap: anywhere;
}
```

40icと1.75は試す値。横幅、字面、読む目的で調整する。長いURLの折り返しを解決する指定は対象へ絞り、和文全体を `break-all` にしない。

## 約物と和欧間隔を比較する

関係する項目: C06、C07。字幅を変えるOpenType機能、句読点の空き、和欧の自動間隔は別々に比較する。表示調整のために元の文字列へ空白を一括挿入しない。

```css
@supports (text-spacing-trim: trim-start) {
  .display-title:lang(ja) {
    text-spacing-trim: trim-start;
  }
}

@supports (text-autospace: normal) {
  .mixed-copy:lang(ja) {
    text-autospace: normal;
  }
}
```

「『AI』で作るWebサイト、2026年11月。」など、括弧・英字・数字を含む実文を比較する。`@supports` は構文を受理するかの検査であり、望む組版になる保証ではない。対象フォントが変わった場合と、指定を外した場合も見る。

## 日本語入力を受ける欄を組み立てる

関係する項目: F03、F06、F07。下の郵便番号は日本国内向けの例。対象地域と保存先の仕様に合わせる。

```html
<label for="postal-code">郵便番号（任意）</label>
<p id="postal-help">例：1000001（数字7桁）</p>
<input
  id="postal-code"
  name="postal-code"
  type="text"
  inputmode="numeric"
  autocomplete="postal-code"
  aria-describedby="postal-help"
/>
```

ハイフンを受け付ける場合、numericキーボードで記号を入力できるか確認する。数字のみを入力する設計にするなら、その形式を入力前に伝え、表示する例も合わせる。先頭の0を落とさず、貼り付けと自動入力を試す。姓・名やふりがなの分割は、見た目の都合だけで追加しない。

## Enterによる独自送信を確認する

関係する項目: F01、F02。独自のEnter送信が不要なら、通常のフォームと送信ボタンを使う。独自に扱う場合は、変換確定Enterと送信を区別する。

```js
function shouldSubmitOnEnter(event) {
  return event.key === 'Enter'
    && !event.shiftKey
    && !event.isComposing
    && event.keyCode !== 229
}
```

この判定関数だけで実フォームの送信を保証できるとは扱わない。実装先では、暗黙のフォーム送信との重複、`preventDefault` の位置、`compositionend` の順序、明示的な送信ボタンを確認する。229は一部環境を扱うための補助で、非推奨APIへの依存が必要かを対象環境で判断する。変換中の入力、候補の確定、確定後の送信、Shift+Enter、モバイルキーボードを実機で確認する。

資料: [GoogleのIME送信ガイド](https://developer.chrome.com/docs/modern-web-guidance/guides/forms/ime-safe-enter-submit)、[デジタル庁の入力欄](https://design.digital.go.jp/dads/components/input-text/usage/)、[CSS Text](https://www.w3.org/TR/css-text-3/)。各ルールの詳しい出典と例外は分野別の資料にある。
