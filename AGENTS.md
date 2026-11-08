# Japanese Web Design

日本語Web UIの仕上げを補助するAgent Skillと、同じ資料を読む静的ガイド。

- `catalog.json` が知見の編集元。`skills/japanese-web-design/references/` の分野別資料と出典一覧は `python3 scripts/package.py render` で生成する。
- `SKILL.md`、カタログ、`package.json` のバージョンを揃える。リリース済みタグを上書きしない。
- 技術仕様、企業の公開実践、編集上の仮説を区別する。仮説の数値を標準の義務へ変えない。
- 変更前に `docs/release-plan.md` と対象の仕様を確認する。新しい条件は代表・境界・反例を含めて検証する。
- `bun run build`、`bun run test` を実行する。表示や操作を変えたらブラウザでも確認する。機密情報、第三者の本文、フォント本体を配布物へ加えない。
- 公開手順は `docs/releasing.md`。サイト配信は既存のWrangler認証と明示したnandaronaアカウントを使う。新しいログインや別アカウントへの切替を自動で行わない。
