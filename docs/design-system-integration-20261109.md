# 共通デザインの原則をWebガイドへ合流する

2026-11-09、本人は残りのデザインシステムを他のLabも含めて本番反映・表示確認まで進めるよう依頼した。本体の余白→面→線、枠のないメニュー、文章のまとまり、44px操作をこのガイドへ適用する。紙色・緑・明朝の見本と、64項目・39資料・v1.0.1のスキル配布物は保持する。

## 観測と完成状態

変更前の本番は横はみ出しとbalance指定が0。一方、ヘッダーのホームは37px、3つのメニューは約40pxで、共通の44px操作より小さかった。ガイド本文と比較例が同じ背景で連続している。フロート型ヘッダー、読み物の面、控えめな補足面へ役割を分け、本文と同じ外幅へそろえる。狭幅ではヘッダーを通常フローへ戻し、長いメニューが体験を覆わない。

## 不変条件と検証

- DSH1: 主要ナビ・フィルター・リセット・コピーの押せる領域は44px以上。長い日本語と320/390/768/1280pxで横にはみ出さない。メニューごとの囲い線は追加しない。
- DSH2: ページ・ガイド・導入・展開項目の面は意味トークンへ結ぶ。比較見本の前後差分はそのまま保持し、サイト全体へ見本の組版を広げない。節間を節内の見出しと本文より広くする。
- DSH3: カタログ、見本の文章、meta/JSON-LD/canonical、検索・カテゴリ・リンク・導入コマンドとZIPの内容を保持する。balance・停止ボタンを追加しない。配布物を更新しないため公開タグやZIPの版は変更しない。Webの表示変更は別のcommitと配備版で追跡する。
- DSH4: ヘッダー・ガイド・導入・フッターの外幅は同じwrap。PCのアンカーをヘッダーで隠さず、狭幅はヘッダーを固定しない。検索後の件数・0件・リセット・詳細開閉・コピーを実際に操作する。

有限の64項目・ファイル集合は既存の全列挙を再利用する。表示は接続済みChromeの実DOM、算出スタイル、実テキスト矩形と画面で検査する。DSH1の変更前違反をRedとし、実装後に同じ判定をGreenへする。操作領域と面のガードを外したCSS変種でも同じ判定が失敗することを確認して元へ戻す。並行処理・認証・DBを変更しないため新しいZ3/TLA+は追加しない。OSごとの字形・実IME・読み上げの全組合せや改善率は保証しない。

## 配備と復旧

必須build/test、機密検査、変更前後の配布物一致、PR CIの成功後にマージする。nandaronaの既存接続と固定Wranglerで同じWorkerへ配備し、本番のCSS・HTML・ZIPと実画面を読み戻す。重大な操作不能や内容欠落は停止条件とし、既存のv1.0.1公開commitを再検証して再配備する。認証・課金・権限・配布タグは変更しない。

## 実行結果

変更前の実Chromeで、ホーム37px・メニュー約40px・分野約38px・コピー約42pxを同じDSH1判定が拒否した。変更後は320/390/768/1280pxの全4幅で主要操作が44px以上、横はみ出し0、balance指定0、ヘッダーと本文の外幅が一致した。320/390はrelative、768/1280はstickyだった。PCのガイド見出しはヘッダー下端84pxより下に表示された。

検索IMEは2件、分野との交差は1件、存在しない語は0件案内、リセットは64件へ戻った。T04の詳細開閉と導入コマンドのコピー成功を確認した。操作領域を約24pxへ縮めた実CSS変種はDSH1、4面を同じ色へ戻した実CSS変種はDSH2でそれぞれ拒否された。構文や依存不足の失敗ではない。変種後は正常CSSの全byteを復元し、最終buildを実行した。

変更前後のHTMLの全テキスト、id・リンク・操作属性とheadは一致した。catalog.json、app.js、llms.txt、sitemap、robots、404、security headers、配布ZIPとSHA-256は全byte一致。既存15 Python検査と3検索検査が成功した。これらは有限な実DOM・実ファイルの検査で、利用者試験や全ブラウザの保証には広げない。

実ブラウザで使ったDSH1/DSH2の判定は次の通り。変更前・2つの実CSS変種・復元後で同じ条件を使い、ページの実DOMと算出値を入力にする。

```js
const targets = [...document.querySelectorAll('header a,.filter,.reset,.copy-button')]
  .filter(e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden')
if (targets.some(e => e.getBoundingClientRect().height < 44)) throw Error('DSH1 touch target below44')
if (document.documentElement.scrollWidth > innerWidth) throw Error('DSH1 overflow')
const surfaces = ['--surface-page', '--surface-guide', '--surface-section', '--surface-detail']
  .map(p => getComputedStyle(document.documentElement).getPropertyValue(p).trim())
if (surfaces.some(v => !v) || new Set(surfaces).size < 3) throw Error('DSH2 semantic surfaces missing')
```

Chromeの拡大キーも試したが、この接続ではdevicePixelRatioとinnerWidthが変わらず、200%拡大の成功とは扱わなかった。4幅の通常表示と折り返しの確認を、OSの文字拡大や全ブラウザの検証の代わりにしない。拡大操作は解除した。
