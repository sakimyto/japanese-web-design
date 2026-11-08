# 公開と復旧

編集元はこのrepository。スキルとWebガイドを同じバージョンのデータから生成する。リリース済みタグと配布ZIPを上書きせず、修正には新しいバージョンを使う。

## 公開前

1. `catalog.json`、`SKILL.md`、`package.json` のバージョンを合わせる。
2. `bun run build` と `bun run test` を実行する。
3. JSON・JavaScriptのBiome検査、日本語の推敲、機密検査を行う。
4. `bun run dev` で表示し、320・375・768・1280px幅、検索と分野の交差条件、詳細の開閉、コピーを確認する。作成した検証タブは終了時に閉じる。
5. skills CLIで隔離したプロジェクトへ導入し、配布フォルダの内容と比較する。既存のユーザー設定やグローバルスキルへ上書きしない。
6. 対象commitをpushし、CIを確認する。

## リリース

`python3 scripts/package.py pack` でZIPとSHA-256を生成する。検証済みcommitにタグを付け、GitHub ReleaseへZIPと照合ファイルを添付する。公開後に匿名で取得し、ローカルのZIPとSHA-256を比較する。タグを指定したCLI導入も実際に試す。

Webガイドは `bun run deploy` でCloudflare Workersへ配備する。Worker名は `japanese-web-design`、公開先は `japanese-design.sakimyto.com`。アカウントは `wrangler.jsonc` のnandaronaに固定する。

2026-11-08の環境では、cf CLIに認証がなく、既存のWrangler OAuthでは対象アカウントへの接続を確認できた。新しいログインや認証情報の移し替えを行わず、Wrangler 4.158.0を固定して使う。cloudflare.config.tsを使うcfへの移行は、認証と静的ビルドの連携を別途確認してから行う。

公開後は、トップ、CSS・JS、カタログ、ZIP、照合ファイル、存在しないURLの404、セキュリティヘッダー、実験への戻りリンクを読み戻す。sakimyto.comのラボ登録とSEO生成は、そのrepositoryの必須CI・配備手順で公開する。

## 復旧

入力の損失、操作不能、資料やZIPの取り違え、意図しない情報公開を重大な問題として扱う。最初の公開には旧バージョンがないため、問題のある導入案内と配布を一時停止して修正版を用意する。旧公開版がある場合は、そのタグを別の一時的な作業領域で検証して再配備する。

GitHubのタグをforceで動かさない。修正の内容、確認したcommit、配布物のハッシュ、配備結果を `docs/verification.md` に残す。新しい認証や権限が必要なら、自動で別アカウントへ切り替えない。
