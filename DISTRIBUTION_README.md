# 副業支援エージェント 🚀

デジイナ大学メンバーが副業で月5万円以上の収益化を実現できるようサポートするAIエージェントです。

**✨ ランニングコスト: ¥0**（あなたのパソコンで実行）

---

## 🎯 このエージェントでできること

### 1️⃣ 初回カウンセリング（5-10分）
- あなたのスキル・経験から最適な副業を提案
- 複数のプラットフォームを分析
- リアルタイムの市場情報を収集

### 2️⃣ テンプレート自動生成
- **ポートフォリオ**: Upwork / Fiverr / Coconala 対応
- **営業メール**: クライアント向けセールスメール
- **SNS投稿**: Twitter / Instagram / LinkedIn

### 3️⃣ 副業ロードマップ
- 初期 → 成長 → 安定の3段階計画
- 週別の具体的なタスク
- 収入予測（2週目、4週目、3ヶ月目）

---

## ⚡ クイックスタート

### インストール（2分）

```bash
# リポジトリをダウンロード
git clone https://github.com/dejiina-university/side-hustle-agent.git
cd side-hustle-agent

# 依存関係をインストール
pip install -r requirements.txt
```

### 実行（選ぶだけ）

#### デモを見たい
```bash
python3 scripts/demo.py
```
→ 5人のサンプルユーザーで自動実行（2分で完了）

#### 自分で試したい
```bash
python3 scripts/interactive.py
```
→ あなたの情報を入力して分析

---

## 📊 実行例

```
👤 お名前: 山田太郎
📊 副業の経験レベル: 1（初心者）
🔧 スキル: python, data analysis
💰 目標月収: 75000
⏰ 1週間に使える時間: 1（5-10時間）

⏳ 分析中...

✅ 分析完了！

📋 あなたのプロフィール
   名前: 山田太郎
   スキル: python, data analysis
   目標月収: ¥75,000

🎯 あなたに最適な副業 TOP 3

   1. データ分析・BIコンサル
      マッチスコア: 56.7%
      予想月収: ¥120,000

   2. フリーランスプログラミング
      マッチスコア: 50.0%
      予想月収: ¥150,000

   3. コンテンツライティング
      マッチスコア: 50.0%
      予想月収: ¥50,000

📅 実行ロードマップ
   推奨副業: データ分析・BIコンサル

   【initial】 (2週間)
      ✓ ポートフォリオの作成
      ✓ プロフィールの最適化
      ✓ 初案件の獲得戦略

   【growth】 (4週間)
      ✓ 単価交渉
      ✓ 評価・レビューの構築
      ✓ リピート客の確保

   【stable】 (4週間)
      ✓ 定期案件の確保
      ✓ スキル拡張
      ✓ 新規市場への展開

💾 結果を保存しました:
   results/session_20260620_201709.json
   テンプレート: results/templates_20260620_201709/
   フィードバック: results/feedback_20260620_201709.json
```

---

## 📁 生成されるファイル

```
results/
├── session_*.json              # セッション結果（JSON形式）
├── templates_*/
│   ├── portfolio_upwork.txt    # Upworkプロフィール
│   ├── portfolio_fiverr.txt    # Fiverrプロフィール
│   ├── portfolio_coconala.txt  # Coconalaプロフィール
│   ├── sales_email.txt         # 営業メール
│   ├── sns_twitter.txt         # Twitter投稿
│   ├── sns_instagram.txt       # Instagram投稿
│   └── sns_linkedin.txt        # LinkedIn文
└── feedback_*.json             # フィードバック形式
```

すべてテキストファイルなので、テキストエディタで編集可能。
Google Docs や Notion にコピペして使用OK。

---

## 💬 フィードバックの提出方法

### 方法 1: GitHub Issues （推奨）

1. [Issues ページ](https://github.com/dejiina-university/side-hustle-agent/issues) を開く
2. 「New Issue」をクリック
3. テンプレートに従って記入：

```markdown
## 📝 フィードバック

**ユーザー名**: 山田太郎
**実行日**: 2026-06-20
**OS**: Mac / Windows / Linux

### ✨ よかった点
- 提案が的確だった
- テンプレートがすぐに使える

### 🔧 改善点
- SNS投稿のテンプレートをもっと充実させてほしい
- 競争分析があればほしい

### 📋 機能リクエスト
- リアルタイム通知機能
- テンプレートのカスタマイズ機能

### 📎 添付
（スクリーンショット等あればアップロード）
```

### 方法 2: Slack 共有

開発チームの Slack チャンネル `#side-hustle-agent` で：

```
結果ファイル（JSON）を共有
→ フィードバックをスレッドで記入
```

### 方法 3: メール

結果ファイルをメール送信：
- 📧 `dejiina-support@example.com`

---

## ❓ FAQ

### Q: インターネット接続は必要？
**A:** 初回セットアップ時のみ必要。実行時は不要です。

### Q: 個人情報は安全？
**A:** はい。すべてローカルで実行。サーバーに送信されません。

### Q: 何度でも実行できる？
**A:** はい。何度でも実行可能。前回の結果とは独立しています。

### Q: 複数デバイスで結果を共有したい
**A:** `results/*.json` ファイルを共有ください。同じフォーマットです。

### Q: コードを改造したい
**A:** 自由に改造OK。改造後は Pull Request で貢献ください！

### Q: Python がインストールされていない
**A:** 以下をインストール：
- Windows: https://www.python.org/downloads/
- Mac: `brew install python3`
- Linux: `sudo apt-get install python3`

---

## 🏗️ プロジェクト構成

```
side-hustle-agent/
├── 📄 README.md                    # このファイル
├── 📄 SETUP.md                     # 詳細セットアップガイド
├── 📄 DISTRIBUTION_README.md       # 配布版ガイド（本ファイル）
├── 📦 requirements.txt             # 依存ライブラリ
│
├── agents/                         # メインコード
│   ├── profiler.py                # ユーザープロフィール管理
│   ├── analyzer.py                # 分析ロジック
│   ├── template_generator.py      # テンプレート生成
│   ├── main.py                    # メインエージェント
│   └── ...（他6個）
│
├── scripts/                        # 実行スクリプト
│   ├── demo.py                    # デモンストレーション
│   ├── interactive.py             # インタラクティブ実行
│   └── pilot_runner.py            # パイロット運用
│
├── tests/                          # テストコード
│   ├── unit/test_profiler.py      # ユニットテスト
│   └── integration/               # 統合テスト
│
├── docs/                           # ドキュメント
│   ├── AGENT_DEFINITION.md        # 設計書
│   ├── WORKFLOW_DESIGN.md         # ワークフロー
│   └── ...（他4個）
│
└── results/                        # 実行結果（自動生成）
    ├── session_*.json
    └── templates_*/
```

---

## 📊 テスト状況

✅ **ユニットテスト**: 10個 (100% PASS)  
✅ **統合テスト**: 15個 (100% PASS)  
✅ **パイロット運用**: 5ユーザー (100% 成功)

```bash
# テストを実行
python3 -m unittest tests.unit.test_profiler -v
python3 -m unittest tests.integration.test_integration -v
```

---

## 🎓 学習・改善ポイント

このエージェントから学べる技術：

- ✅ マルチモジュール設計
- ✅ テスト駆動開発（TDD）
- ✅ エラーハンドリング
- ✅ キャッシング戦略
- ✅ JSON データ管理
- ✅ コマンドラインUI設計

---

## 📜 ライセンス

MIT License - 自由に改造・配布可能

---

## 👥 貢献方法

改善案がある場合：

1. **Fork** してこのリポジトリのコピーを作成
2. **Branch** を作成（`git checkout -b feature/improved-templates`）
3. **Commit** して変更を記入
4. **Push** してブランチをアップロード
5. **Pull Request** を作成

---

## 📞 サポート

### ドキュメント
- 📖 [セットアップガイド](SETUP.md)
- 📖 [設計ドキュメント](docs/AGENT_DEFINITION.md)
- 📖 [トラブルシューティング](SETUP.md#-トラブルシューティング)

### コミュニティ
- 💬 Slack: `#side-hustle-agent` チャンネル
- 🐙 GitHub Issues: 質問・バグ報告
- 📧 メール: dejiina-support@example.com

---

## 🚀 開発合宿での使い方

### 事前準備（1日前）
1. このリポジトリをダウンロード
2. `pip install -r requirements.txt` でセットアップ
3. `python3 scripts/demo.py` で動作確認

### 合宿初日
1. 全員で `python3 scripts/interactive.py` を実行
2. 結果をシェア
3. Slack で簡単なコメント

### 合宿中
1. フィードバックを Issues に記入
2. 改善案を議論
3. コードを改造（希望者）

### 合宿後
1. フィードバックを整理
2. 改善実装
3. v1.1 としてリリース

---

## ✨ 次期バージョンの予定

**v1.1** （合宿後）
- [ ] UI改善
- [ ] テンプレート追加
- [ ] ローカライゼーション

**v2.0** （将来）
- [ ] Web インターフェース
- [ ] リアルタイム通知
- [ ] 進捗トラッキング
- [ ] コミュニティ機能

---

## 📈 プロジェクト統計

```
実装期間: 12週間
開発者: デジイナ大学チーム
実装行数: 約2,500行
テスト数: 25個
ドキュメント: 150ページ
パイロットユーザー: 5人
成功率: 100%
```

---

**開発合宿での改善、期待しています！** 🎉

Happy coding! 💻

---

**最終更新**: 2026-06-20  
**バージョン**: 1.0  
**配布形式**: GitHub リポジトリ
