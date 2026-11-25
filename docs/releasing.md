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

Webガイドと旧ホスト `japanese-design.sakimyto.com` の転送は sakimyto.com の本体アプリ（nandarona-inc/sakimytocom、Worker `sakimyto-dev`）にある。新しい版をリリースしたら、そのタグの `catalog.json` をアプリの `public/japanese-web-design/catalog.json` へ取り込み、アプリ側のテストが持つSHA-256を同じ変更で更新する。このrepositoryからCloudflare Workerを配備することはない（旧Worker設定は2026-11-25に廃止。緊急ロールバックが必要な場合のみ commit `891bc49` から `wrangler.jsonc` と `worker/index.js` を復元する）。設計は [ガイドを sakimyto.com の下で配信する](serve-under-sakimyto-com-20261120.md) の「本体アプリへの取り込み」。

旧ホストの転送とガイドの表示は、アプリ側repositoryのCIと配備後の `node scripts/verify-legacy-japanese-design.mjs --live --check-owner` で読み戻す。

## 復旧

入力の損失、操作不能、資料やZIPの取り違え、意図しない情報公開を重大な問題として扱う。配信の場所を戻すときは、[ガイドを sakimyto.com の下で配信する](serve-under-sakimyto-com-20261120.md) の「公開の順序と復旧」に従い、sakimyto.com の記録を先に戻してから再配備し、経路を読み戻す。最初の公開には旧バージョンがないため、問題のある導入案内と配布を一時停止して修正版を用意する。旧公開版がある場合は、そのタグを別の一時的な作業領域で検証して再配備する。

GitHubのタグをforceで動かさない。修正の内容、確認したcommit、配布物のハッシュ、配備結果を `docs/verification.md` に残す。新しい認証や権限が必要なら、自動で別アカウントへ切り替えない。
