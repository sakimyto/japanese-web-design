# 公開と復旧

編集元はこのrepository。スキルとWebガイドを同じバージョンのデータから生成する。リリース済みタグと配布ZIPを上書きせず、修正には新しいバージョンを使う。

## 公開前

1. `catalog.json`、`SKILL.md`、`package.json` のバージョンを合わせる。
2. `bun run build` と `bun run test` を実行する。
3. JSON・JavaScriptのBiome検査、日本語の推敲、機密検査を行う。
5. skills CLIで隔離したプロジェクトへ導入し、配布フォルダの内容と比較する。既存のユーザー設定やグローバルスキルへ上書きしない。
6. 対象commitをpushし、CIを確認する。

## リリース

`python3 scripts/package.py pack` でZIPとSHA-256を生成する。検証済みcommitにタグを付け、GitHub ReleaseへZIPと照合ファイルを添付する。公開後に匿名で取得し、ローカルのZIPとSHA-256を比較する。タグを指定したCLI導入も実際に試す。

Webガイドは sakimyto.com のアプリ（nandarona-inc/sakimytocom）にある。新しい版をリリースしたら、そのタグの `catalog.json` をアプリの `public/japanese-web-design/catalog.json` へ取り込み、アプリ側のテストが持つSHA-256を同じ変更で更新する。このrepositoryのWorker `japanese-web-design` は、旧ホスト `japanese-design.sakimyto.com` の要求を新しいURLへ301で転送するだけである。転送の対応を変えたときだけ `bun run deploy` で配備する。設計は [ガイドを sakimyto.com の下で配信する](serve-under-sakimyto-com-20261120.md) の「本体アプリへの取り込み」。アカウントは `wrangler.jsonc` のnandaronaに固定する。

2026-11-08の環境では、cf CLIに認証がなく、既存のWrangler OAuthでは対象アカウントへの接続を確認できた。新しいログインや認証情報の移し替えを行わず、Wrangler 4.158.0を固定して使う。cloudflare.config.tsを使うcfへの移行は、認証と静的ビルドの連携を別途確認してから行う。

Workerを配備したら、旧ホストの各パスが1回の301で届き、`robots.txt` が200になることを読み戻す。ガイドの表示は、アプリのrepositoryの必須CI・配備手順で公開し、`https://sakimyto.com/japanese-web-design` を読み戻す。

## 復旧

入力の損失、操作不能、資料やZIPの取り違え、意図しない情報公開を重大な問題として扱う。配信の場所を戻すときは、[ガイドを sakimyto.com の下で配信する](serve-under-sakimyto-com-20261120.md) の「公開の順序と復旧」に従い、sakimyto.com の記録を先に戻してから再配備し、経路を読み戻す。最初の公開には旧バージョンがないため、問題のある導入案内と配布を一時停止して修正版を用意する。旧公開版がある場合は、そのタグを別の一時的な作業領域で検証して再配備する。

GitHubのタグをforceで動かさない。修正の内容、確認したcommit、配布物のハッシュ、配備結果を `docs/verification.md` に残す。新しい認証や権限が必要なら、自動で別アカウントへ切り替えない。
