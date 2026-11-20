# ガイドを sakimyto.com の下で配信する（2026-11-20）

本人の依頼「sakimyto.comの下においたほうがよくないかい」「同一サービス内にのせたほうがよいならのせる」に基づく。公開ガイドの場所を `https://japanese-design.sakimyto.com/` から `https://sakimyto.com/japanese-web-design/` へ移す。

## 決めたこと

このrepositoryとWorkerは分けたままにし、配信する経路だけを sakimyto.com へ向ける。sakimyto.com のアプリへは取り込まない。

- ガイドはリンクされて検索される資料なので、実験の記録（`/lab/japanese-web-design`）と同じホストに置く。パスは実験の識別子・repository・スキルの名前と同じ `japanese-web-design` にする。
- カタログの編集元はこのrepositoryで、スキルとガイドを同じ版から生成する。本体のrepositoryに残る同梱版は0.1.1のままで、写しを2か所に持つと版がずれる。
- 紙色・緑・明朝の見本というガイド固有の見た目を保つ。本体の文字や色の体系と並立させない。

v1.0.1 のスキル、ZIP、タグは変えない。ZIPとスキル本文は旧URLを含まない。

## URLの対応

| 旧URL（japanese-design.sakimyto.com） | 応答 |
| --- | --- |
| `/`、`/for-ai/`、`/llms.txt`、`/catalog.json`、`/style.css`、`/app.js`、`/sitemap.xml`、v1.0.1 のZIPと照合ファイル | 301 で `https://sakimyto.com/japanese-web-design` に同じパスを続けた先へ |
| v1.0.0 のZIPと照合ファイル | 301 で GitHub Release v1.0.0 の同じファイルへ（ビルドは現行の版だけを出力する） |
| `/robots.txt` | 200。全パスの取得を許可し、巡回が転送を読めるようにする |
| そのほかのパス | 301 で同じパスを続けた先へ。転送先で 404 になる |

クエリは転送先へ引き継ぐ。転送先のホストは固定で、パスの内容によって別のホストへ向かない。

`robots.txt` はホストの最上位でしか読まれないので、新しい場所には出力しない。`sitemap.xml` は `/japanese-web-design/sitemap.xml` に置き、sakimyto.com の `robots.txt` から参照する。

## 配信の構成

Worker `japanese-web-design` が2つの経路を受ける。

- `sakimyto.com/japanese-web-design*`（末尾の `*` がスラッシュ以降とクエリ付きの入口を含むので、経路は1本）: 静的アセットを `assets.base_path` で `/japanese-web-design` の下に公開する。`_headers` の規則も公開パスで書く。
- `japanese-design.sakimyto.com`: Workerのスクリプト（`worker/index.js`）が上の表のとおり応答する。

`run_worker_first` は `/japanese-web-design/` の下を除く全パスにする。ガイドのファイルはスクリプトを通らずに配信され、`_headers` がそのまま付く。Cloudflareの資料は、スクリプトが作った応答に `_headers` が付かないと注意しているため、ファイルの配信をスクリプトへ通さない。

受け入れた残り: 旧ホストの `/japanese-web-design/` の下は、スクリプトを通らず同じファイルを返す。どこからもリンクしておらず、canonical は新しいURLを指す。

受け入れた残り: 経路 `sakimyto.com/japanese-web-design*` は、クエリ付きの入口を受けるために末尾を `*` にしている。`/japanese-web-designer` のように同じ文字で始まる別のパスもこのWorkerに届き、404 を返す。

受け入れた残り: スクリプトを通る応答には `_headers` が付かない。該当するのは、末尾スラッシュなしの `/japanese-web-design` の 307、上の別パスの 404、旧ホストの 301 と `robots.txt` で、どれもページの本文を持たない。

公開元・パス・旧ホストは `site.config.json` に置き、ビルド、Worker、テストが同じ値を読む。

## 不変条件と検証

対象は有限のファイルとURLなので全列挙で確かめる。並行する状態はなく、Z3やTLA+は使わない。

| ID | 不変条件 | 方法 |
| --- | --- | --- |
| BASE | 生成した全HTMLの、`/` で始まる `href`・`src` は `/japanese-web-design/` の下にある | 生成物の全属性を列挙。パスを付け忘れた変種を検出する |
| ORIGIN | 生成した全テキストに旧ホストが現れず、canonical・og:url・JSON-LD・sitemap・llms.txt が新しいURLを指す | 生成物の全ファイルを走査 |
| LEGACY | 旧ホストへの要求は、`robots.txt` を除き全て 301 になり、転送先は `https://sakimyto.com/japanese-web-design` で始まるか、v1.0.0 のGitHub Releaseである | 本番で 200 を確認した全パスと、クエリ・未知のパス・二重スラッシュ・パス区切りの組み合わせを列挙。パスを落とす変種と、新しいホストを転送する変種を検出する |
| PRIMARY | 新しいホストへの要求をスクリプトは転送せず、アセットへ渡す | 同じ入力の列挙 |
| CONFIG | `wrangler.jsonc` の経路・`base_path`・`run_worker_first` が `site.config.json` と一致する | 設定ファイルを読んで照合 |
| PACKAGE | v1.0.1 のZIPのSHA-256 は公開済みの値と同じ | ビルドしたZIPを `docs/release-evidence.json` の値と照合 |

保証するのは、生成物の内容、転送の対応、設定の一致まで。Cloudflare上の経路の優先順位、実際の応答ヘッダー、検索エンジンでの扱いは、配備後に本番で読み戻す。検索流入の増加は保証しない。

## 公開の順序と復旧

1. このrepositoryを配備する。新しいURLが 200、旧URLが 301 になることを本番で読み戻す。
2. sakimyto.com のrepositoryで、実験の記録のリンク先と `robots.txt` を更新して公開する。

1 の後、2 の前でも、本体の記録からの旧リンクは 301 で新しいURLへ届く。

復旧は、公開と逆の順で行う。

1. sakimyto.com のrepositoryで、記録のリンク先を旧URLへ戻す変更を公開する。
2. このrepositoryで、移す前のcommitを別の作業領域に取り出し、ビルドして再配備する。
3. Cloudflareの画面かAPIで、Worker `japanese-web-design` の経路を読み戻す。`sakimyto.com/japanese-web-design*` が残っていれば外す。`wrangler deploy` が設定から消えた経路を外すかは確かめていない。

3 を省くと、旧版のファイルが新しいパスで応答する。旧版のリンクは最上位から始まるので、CSS・JS・ページ内のリンクが404になる。301 を受け取ったブラウザは転送を覚えていることがあり、復旧後も新しいパスへ進む。経路を外した後は、そのパスを sakimyto.com のアプリが受けて404を返す。

## ビルドと配備

`build_site.py` は出力先を空にしてから書く。`bun run deploy` は先に `bun run build` を実行する。配備は出力先のフォルダを丸ごと送るので、移す前のビルドが残ると、旧ホスト向けの `robots.txt` や古いZIPが新しいパスで公開される。

## ローカルでの確認（2026-11-20）

Wrangler 4.158.0 の `dev --local` を、ホストを切り替えて2回起動して読んだ。本番の経路とは別の確認である。

- 新しいホスト: `/japanese-web-design/` と `for-ai/`、CSS、JS、カタログ、`llms.txt`、`sitemap.xml`、ZIP、照合ファイルが 200。`_headers` のCSPと `X-Frame-Options` が付く。末尾スラッシュなしは 307 でスラッシュ付きへ、存在しないパスは 404 ページ。
- 旧ホスト: 本番で 200 を返していた11パスと `/for-ai`、クエリ付き、未知のパスが 301、`robots.txt` が 200。v1.0.0 の転送先は GitHub Release で 200、ZIPのSHA-256は旧ホストで配信中のものと同じ `f151a7cd…b889`。
- ブラウザ: 新しいパスでスタイルと検索が動く（64項目、「IME」で2件）。コンソールのエラーなし。

テストは Python 24件、Node 6件。旧ホストの転送は392通りの境界入力と、壊した5つの変種で確かめた。各変種は、その欠陥を名指しする検査で落ちることまで照合する。
