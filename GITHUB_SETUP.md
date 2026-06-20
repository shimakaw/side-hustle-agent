# GitHub 公開手順ガイド

このエージェントを GitHub で公開するための完全ガイドです。

---

## 📋 事前準備

### 必要なもの
- [ ] GitHub アカウント（なければ無料登録）
- [ ] Git がインストール済み
- [ ] GitHub にログイン状態

### 確認事項
- [ ] `.gitignore` が設定されている（✅ 済み）
- [ ] `LICENSE` が設定されている（✅ 済み）
- [ ] `README.md` が存在する（✅ 済み）
- [ ] `SETUP.md` が存在する（✅ 済み）

---

## 🚀 公開手順（5ステップ）

### Step 1: GitHub で新しいリポジトリを作成

1. https://github.com/new にアクセス
2. 以下を入力：

```
Repository name: side-hustle-agent

Description: 
デジイナ大学メンバーが副業で月5万円以上の収益化を実現できるようサポートするAIエージェント

Visibility: Public （誰でも見れるように）

Initialize this repository with: （チェックしない）
```

3. 「Create repository」をクリック

### Step 2: ローカルでリポジトリを初期化

```bash
cd /Users/macmini2022/claude-work/デジイナ大学/products/018_side_hustle_agent

# Git を初期化
git init

# リモートを追加（XXX = あなたの GitHub ユーザー名）
git remote add origin https://github.com/XXX/side-hustle-agent.git

# ブランチを main に変更
git branch -M main
```

### Step 3: すべてのファイルを追加

```bash
# ファイルを確認（確認用）
git status

# 不要なファイルが含まれていないか確認
# .DS_Store、__pycache__、results/ などが含まれていないはず

# ファイルを追加
git add .
```

### Step 4: 初回コミット

```bash
git commit -m "初回公開: 副業支援エージェント v1.0

- コア機能：10モジュール
- テスト：25個（100% PASS）
- ドキュメント：7個
- ランニングコスト：¥0

開発合宿用の配布版です。
フィードバックをお待ちしています！"
```

### Step 5: GitHub に push

```bash
git push -u origin main
```

**完了！** 🎉

---

## 🔗 公開後の確認

### リポジトリ URL
```
https://github.com/[あなたのユーザー名]/side-hustle-agent
```

### 確認項目
- [ ] README.md が表示されている
- [ ] ファイルが全て公開されている
- [ ] `.gitignore` が機能している（`results/` が含まれていない）
- [ ] LICENSE が表示されている

---

## 👥 開発合宿メンバーへの共有

### 方法 1: GitHub リンク共有（推奨）

```
【Slack チャンネルに投稿】

🚀 副業支援エージェント v1.0 が完成しました！

GitHub: https://github.com/[ユーザー名]/side-hustle-agent

【セットアップ】
$ git clone https://github.com/[ユーザー名]/side-hustle-agent.git
$ cd side-hustle-agent
$ pip install -r requirements.txt
$ python3 scripts/demo.py

【フィードバック】
GitHub Issues でお待ちしています！
https://github.com/[ユーザー名]/side-hustle-agent/issues

開発合宿で一緒に改善しましょう！ 🎉
```

### 方法 2: メール共有

```
件名: 副業支援エージェント - 開発合宿用

本文:

こんにちは！

副業支援エージェントが完成しました。
開発合宿でのフィードバックをお待ちしています。

📦 ダウンロード
https://github.com/[ユーザー名]/side-hustle-agent

📖 セットアップガイド
https://github.com/[ユーザー名]/side-hustle-agent/blob/main/SETUP.md

💬 フィードバック
GitHub Issues で記入してください

よろしくお願いします！
```

---

## 📊 公開後の管理

### Issues の管理

```bash
# Issue を確認
gh issue list

# コメントに返信
gh issue comment [issue_number] -b "ありがとうございます！検討します"

# Issue をクローズ
gh issue close [issue_number]
```

### 改善実装後の更新

```bash
# 改善内容をコミット
git add .
git commit -m "v1.1: テンプレート追加、UI改善

- SNS投稿テンプレート拡充
- エラーメッセージ改善
- 実行速度最適化

Issue #1, #3, #5 を解決"

# GitHub に push
git push origin main

# リリースを作成（オプション）
gh release create v1.1 -t "v1.1: 改善版" -n "改善内容..."
```

---

## 🎯 GitHub での運用ルール

### Issue の分類

| ラベル | 説明 |
|--------|------|
| `feedback` | ユーザーからのフィードバック |
| `bug` | バグ報告 |
| `enhancement` | 機能改善 |
| `question` | 質問 |
| `documentation` | ドキュメント関連 |

### レスポンス時間

- 🟢 **緊急** (バグ): 24時間以内
- 🟡 **重要** (機能追加): 1週間以内
- 🟠 **その他**: 2週間以内

---

## 💡 ベストプラクティス

### README を充実させる

```markdown
# Side Hustle Support Agent

短い説明（1文）

## 🎯 できること
- xxx
- xxx

## ⚡ クイックスタート
```

### Star をもらうために

1. ✅ わかりやすい README
2. ✅ 充実したドキュメント
3. ✅ デモ動画（オプション）
4. ✅ 定期的な更新

### 貢献を促進

```markdown
## 🤝 貢献方法

Fork してコードを改造 → Pull Request

詳細は CONTRIBUTING.md を参照
```

---

## 🔒 セキュリティ設定

### GitHub の設定

1. **Settings** → **Security & Analysis**
   - [ ] Dependabot alerts: ON
   - [ ] Dependabot security updates: ON
   - [ ] Secret scanning: ON

2. **Settings** → **Branch protection rules**
   - [ ] Require pull request reviews before merging
   - [ ] Require status checks to pass before merging

---

## 📈 公開後のチェックリスト

- [ ] リポジトリが公開されている
- [ ] README が表示されている
- [ ] セットアップ手順が実行可能
- [ ] デモが正常に動作
- [ ] Issue テンプレートが機能している
- [ ] License が表示されている
- [ ] メンバーに共有完了
- [ ] フィードバック収集準備完了

---

## 📞 トラブルシューティング

### Q: `git push` でエラーが出た

**A:** リモート URL を確認
```bash
git remote -v

# 間違っていれば修正
git remote set-url origin https://github.com/[正しいURL].git
```

### Q: ファイルが多すぎてエラーになった

**A:** `.gitignore` が機能していない可能性
```bash
# 不要なファイルを削除
rm -rf __pycache__ .DS_Store results/

# キャッシュをクリア
git rm -r --cached .

# 再度追加
git add .
git commit -m "キャッシュクリア"
git push
```

### Q: 間違えてプッシュしてしまった

**A:** 最新コミットを取り消す（公開前なら）
```bash
git reset HEAD~1
git push --force origin main
```

---

## 🎉 公開完了！

これでエージェントが公開されました！

### やること
1. ✅ メンバーに共有
2. ✅ フィードバック収集
3. ✅ 改善実装
4. ✅ v1.1 リリース

---

**GitHub での公開、成功を祈っています！** 🚀

---

**最終更新**: 2026-06-20  
**対象**: 公開準備
