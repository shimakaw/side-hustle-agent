# 🚀 副業支援エージェント - セットアップガイド

**開発合宿メンバー向け**

このエージェントは **あなたのパソコンで実行** します。クラウド不要、ランニングコストなし。

---

## ⚡ クイックスタート（3ステップ）

### Step 1: リポジトリをダウンロード

```bash
# ターミナル/コマンドプロンプトを開いて実行
git clone https://github.com/dejiina-university/side-hustle-agent.git
cd side-hustle-agent
```

または、[ここからZIPダウンロード](https://github.com/dejiina-university/side-hustle-agent/archive/refs/heads/main.zip)

### Step 2: 依存関係をインストール

```bash
# Python 3.9 以上がインストールされていることを確認
python3 --version

# 依存ライブラリをインストール（ほぼなし）
pip install -r requirements.txt
```

### Step 3: エージェントを実行

```bash
# デモンストレーション
python3 scripts/easy_usage.py

# または、インタラクティブモード
python3 scripts/interactive.py
```

**完了！** 📝 結果が `results/` フォルダに保存されます

---

## 📋 詳細セットアップ

### Windows ユーザー

```cmd
# ステップ 1: Python をインストール
# https://www.python.org/downloads/ からダウンロード
# インストール時に「Add Python to PATH」にチェック

# ステップ 2: リポジトリをダウンロード
git clone https://github.com/dejiina-university/side-hustle-agent.git
cd side-hustle-agent

# ステップ 3: 依存関係をインストール
pip install -r requirements.txt

# ステップ 4: 実行
python scripts/easy_usage.py
```

### Mac/Linux ユーザー

```bash
# ステップ 1: Homebrew（Macのみ）で Python をインストール
brew install python3

# ステップ 2: リポジトリをダウンロード
git clone https://github.com/dejiina-university/side-hustle-agent.git
cd side-hustle-agent

# ステップ 3: 依存関係をインストール
pip3 install -r requirements.txt

# ステップ 4: 実行
python3 scripts/easy_usage.py
```

---

## 🎯 使い方

### モード 1: デモンストレーション（推奨）

```bash
python3 scripts/demo.py
```

**内容:**
- 5人のサンプルユーザーで自動実行
- 各ユーザーの推奨副業を表示
- テンプレート生成を実演
- 約2分で完了

### モード 2: インタラクティブ（自分で試す）

```bash
python3 scripts/interactive.py
```

**内容:**
- あなたの情報を入力
- エージェントが分析
- テンプレートを生成
- 結果を JSON ファイルで保存

**入力例:**
```
名前: 田中太郎
経験レベル: 初心者
スキル: python, データ分析
目標月収: 75000
時間的余裕: 週5-10時間
```

### モード 3: テスト実行（開発者向け）

```bash
# ユニットテスト
python3 -m unittest tests.unit.test_profiler -v

# 統合テスト
python3 -m unittest tests.integration.test_integration -v
```

---

## 📝 結果の確認

実行後、以下のファイルが生成されます：

```
results/
├── session_YYYYMMDD_HHMMSS.json      # セッション結果
├── templates_YYYYMMDD_HHMMSS/
│   ├── portfolio_upwork.txt
│   ├── portfolio_fiverr.txt
│   ├── portfolio_coconala.txt
│   ├── sales_email.txt
│   ├── sns_twitter.txt
│   ├── sns_instagram.txt
│   └── sns_linkedin.txt
└── feedback.json                      # フィードバック（後で入力）
```

テキストエディタで開いて確認してください。

---

## 🐛 トラブルシューティング

### Q: `python3 is not found` エラー

**A:** Python がインストールされていません。

```bash
# Windows
https://www.python.org/downloads/ からダウンロード・インストール

# Mac
brew install python3

# Linux（Ubuntu）
sudo apt-get install python3
```

### Q: `ModuleNotFoundError` エラー

**A:** 依存関係をインストールしてください。

```bash
pip3 install -r requirements.txt
```

### Q: ファイルが見つからない

**A:** 正しいディレクトリにいることを確認。

```bash
# 現在のディレクトリを表示
pwd

# フォルダの中身を確認
ls -la

# side-hustle-agent フォルダに移動
cd side-hustle-agent
```

### Q: 実行がめっちゃ遅い

**A:** 初回実行は遅い場合があります。キャッシュが構築されると高速化します。

---

## 💬 フィードバックの提出方法

### 方法 1: GitHub Issues で報告（推奨）

1. [GitHub Issues](https://github.com/dejiina-university/side-hustle-agent/issues) を開く
2. 「New Issue」をクリック
3. 以下を記入：
   ```
   【フィードバック内容】
   - 何がよかった？
   - 何が改善すべき？
   - 機能のリクエスト？
   
   【環境】
   - OS（Windows/Mac/Linux）
   - Python バージョン
   - 実行方法
   
   【スクリーンショット】
   （あれば）
   ```

### 方法 2: フィードバックフォーム

実行後に生成される `results/feedback.json` を編集：

```json
{
  "user_name": "あなたの名前",
  "date": "2026-06-20",
  "overall_rating": 4,
  "comments": {
    "usability": "わかりやすかった",
    "accuracy": "提案が的確だった",
    "improvements": "SNS投稿のテンプレートをもっと充実させてほしい",
    "feature_requests": "リアルタイム通知機能がほしい"
  },
  "environment": {
    "os": "Mac",
    "python_version": "3.9.6"
  }
}
```

### 方法 3: Slack で直接報告

開発チームの Slack チャンネル `#side-hustle-agent` で共有

---

## 📊 よくある質問

### Q: インターネット接続は必要？

**A:** 基本的には不要です。ただし、初期化時にいくつかのパッケージをダウンロードします。

### Q: 個人情報は安全？

**A:** 100%ローカルで実行。サーバーに送信されません。ご安心ください。

### Q: 複数回実行できる？

**A:** はい。何度でも実行可能。

### Q: 他の人のと結果を比較したい

**A:** 結果ファイルを共有してください。フォーマットは同じです。

### Q: コードを改造したい

**A:** 自由に改造できます！改造したら GitHub で Pull Request してください。

---

## 📞 サポート

### ドキュメント

- [README.md](./README.md) - 全体的な説明
- [設計ドキュメント](./AGENT_DEFINITION.md) - 技術仕様
- [FAQ](./FAQ.md) - よくある質問

### 連絡先

- 📧 メール: dejiina-support@example.com
- 💬 Slack: #side-hustle-agent チャンネル
- 🐙 GitHub Issues: 技術的な問題

---

## ✅ チェックリスト

セットアップ完了確認：

- [ ] Python 3.9 以上がインストール済み
- [ ] リポジトリをダウンロード
- [ ] `pip install -r requirements.txt` で依存関係をインストール
- [ ] `python3 scripts/demo.py` で動作確認
- [ ] 結果が `results/` に生成された
- [ ] フィードバックを用意

---

**準備完了！開発合宿で一緒に改善しましょう！** 🚀

---

**最終更新**: 2026-06-20  
**バージョン**: 1.0  
**対象**: デジイナ大学開発チーム
