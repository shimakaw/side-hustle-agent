# 副業支援エージェント - デプロイメント手順書

## 📋 概要

このドキュメントでは、副業支援エージェントを本番環境にデプロイしるまでのステップを詳細に定義します。

**対象環境**: デジイナ大学の Claude Code 環境  
**デプロイメント戦略**: 段階的ロールアウト (段階1→段階2→段階3)

---

## 🚀 デプロイメント戦略

### 全体スケジュール

```
Week 1-2: 準備・検証フェーズ
Week 3-4: パイロット運用 (5ユーザー)
Week 5-6: 段階1 リリース (20ユーザー)
Week 7+: 段階2・3へ拡大
```

---

## 🔧 段階1: 準備フェーズ (Week 1-2)

### 1.1 環境構築

#### 前提条件の確認

```bash
# 1. ディレクトリ構造確認
ls -la /Users/macmini2022/claude-work/デジイナ大学/products/018_side_hustle_agent/

# 期待される構成:
# ├── AGENT_DEFINITION.md
# ├── TOOL_INTEGRATION_SPEC.md
# ├── WORKFLOW_DESIGN.md
# ├── TEST_PLAN.md
# ├── DEPLOYMENT_GUIDE.md
# ├── config.json (後述)
# ├── agents/ (後述)
# ├── tests/ (後述)
# └── README.md (後述)
```

#### ファイル準備

```bash
# 1. メインディレクトリ確認
cd /Users/macmini2022/claude-work/デジイナ大学/products/018_side_hustle_agent/

# 2. 必要なサブディレクトリ作成
mkdir -p agents templates config logs data

# 3. Python 仮想環境作成（オプション、単独実行の場合）
# python -m venv venv
# source venv/bin/activate
```

### 1.2 設定ファイル準備

#### config.json の作成

```json
{
  "version": "1.0",
  "environment": "development",
  "agent": {
    "name": "Side Hustle Support Agent",
    "description": "デジイナ大学メンバー向け副業支援エージェント",
    "version": "1.0.0",
    "author": "デジイナ大学 運営チーム"
  },
  "claude_api": {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 2048,
    "temperature": 0.7,
    "monthly_budget_tokens": 1000000,
    "api_timeout_seconds": 30
  },
  "web_search": {
    "enabled": true,
    "keywords_per_session": 5,
    "fetch_top_results": 5,
    "cache_ttl_days": 7,
    "timeout_seconds": 30,
    "retry_max_attempts": 3
  },
  "local_files": {
    "reference_manifest": "products/MANIFEST.json",
    "ai_fukugyo_research": "products/003_ai_fukugyo/research.md",
    "cache_ttl_days": 30
  },
  "platforms": {
    "upwork": {
      "enabled": true,
      "update_frequency_days": 7,
      "cache_ttl_days": 7
    },
    "coconala": {
      "enabled": true,
      "update_frequency_days": 7
    },
    "crowdworks": {
      "enabled": true,
      "update_frequency_days": 7
    }
  },
  "logging": {
    "level": "INFO",
    "log_dir": "logs",
    "max_file_size_mb": 10,
    "backup_count": 5
  },
  "cache": {
    "enabled": true,
    "backend": "local",
    "directory": "data/cache",
    "default_ttl_hours": 24
  }
}
```

#### 環境変数設定

```bash
# .env ファイル作成（本番環境）
cat > /Users/macmini2022/claude-work/デジイナ大学/products/018_side_hustle_agent/.env << EOF
# Claude API
ANTHROPIC_API_KEY=sk_live_xxxxx_placeholder

# 環境
ENVIRONMENT=production
LOG_LEVEL=INFO

# Web検索
WEB_SEARCH_ENABLED=true
SEARCH_TIMEOUT_SECONDS=30

# キャッシュ
CACHE_ENABLED=true
CACHE_TTL_DAYS=7

# デバッグ
DEBUG=false
EOF

# .env をローカル開発用 .env.local に分離
# （実本番環境では .env を厳重に管理）
```

### 1.3 ドキュメント統合

#### README.md 作成

```markdown
# 副業支援エージェント

**デジイナ大学メンバーが副業で収益化できるようサポートするエージェント**

## 機能

1. **副業機会の発見**: スキル・経験から最適な副業を提案
2. **収益化戦略**: 時給・単価の提案、ポートフォリオ作成支援
3. **プロジェクト管理**: タスク分解、スケジュール管理
4. **クライアント獲得**: 営業テンプレート、SNS戦略

## 利用開始

### 前提条件
- Claude Code 環境へのアクセス
- デジイナ大学メンバー登録

### クイックスタート

```bash
# 1. エージェント起動
/agent-creator  # または direct API call

# 2. 初回カウンセリング
## フォーム入力:
- スキル: [例] Python, Data Analysis
- 経歴: [例] 3年のデータアナリスト
- 利用可能時間: 週10時間
- 目標月収: 50,000円

# 3. 提案取得
副業機会レポートが自動生成されます
```

## ドキュメント

- [エージェント定義](./AGENT_DEFINITION.md): 目的、機能、出力形式
- [ツール統合仕様](./TOOL_INTEGRATION_SPEC.md): API、Web検索連携
- [ワークフロー設計](./WORKFLOW_DESIGN.md): 各ワークフローの詳細
- [テスト計画](./TEST_PLAN.md): テストケース、テスト実行手順
- [デプロイメント](./DEPLOYMENT_GUIDE.md): 本デプロイメント手順

## 使用例

### 初回カウンセリング
```
ユーザー入力 → ローカル情報検索 → Web検索 → 分析 → 提案生成
所要時間: 5～10分
出力: 副業機会レポート (TOP3 + 実行計画)
```

### ポートフォリオ作成
```
フォーム入力 → テンプレート選択 → テンプレート生成 → カスタマイズ
所要時間: 20～30分
出力: Upwork/Coconala対応プロフィール文
```

## FAQ

**Q1: 本当に月5万円稼げるか？**
A: 初心者は月1～2万円が現実的です。3ヶ月で月5万円が目標。

**Q2: どのプラットフォームがおすすめ？**
A: 初心者は「クラウドワークス」「Coconala」から始めることをおすすめします。

**Q3: 単価はどのくらい？**
A: スキル・経歴により異なります。相場情報はレポートに含まれます。

## サポート

問題が発生した場合:
1. [トラブルシューティング](./TROUBLESHOOTING.md) を確認
2. デジイナ大学のサポートチャネルで相談

## ライセンス

デジイナ大学 内部専用

**最終更新**: 2026-06-20
```

### 1.4 テスト環境構築

```bash
# テストディレクトリ作成
mkdir -p tests/unit tests/integration tests/fixtures

# テスト実行スクリプト作成
cat > tests/run_tests.sh << 'EOF'
#!/bin/bash
# テスト実行スクリプト

echo "=== Unit Tests ==="
python -m pytest tests/unit/ -v

echo "=== Integration Tests ==="
python -m pytest tests/integration/ -v

echo "=== Coverage Report ==="
python -m pytest --cov=agents --cov-report=html
EOF

chmod +x tests/run_tests.sh
```

---

## 📦 段階2: パイロット運用 (Week 3-4)

### 2.1 内部テストユーザーの選定

**選定基準**:
- デジイナ大学の中心メンバー 5名
- スキルレベル: 初心者～中級者の混在
- 副業経験: あり・なしの混在
- 使用目的: 多様性を確保

**テスト内容**:
```
週 1-2:
  ├─ 初回カウンセリング体験
  ├─ ポートフォリオ作成支援
  └─ UX/UI フィードバック収集

週 3-4:
  ├─ 営業戦略プラン体験
  ├─ 月次フォローアップシミュレーション
  └─ 改善提案実装
```

### 2.2 フィードバック収集

#### フォーマット

```
【ユーザー: 名前】
【日付: YYYY-MM-DD】

【実施した操作】
- 初回カウンセリングを実行

【良かった点】
- スキル入力フォームがわかりやすかった
- 提案内容が具体的だった

【改善点】
- Web検索の時間がかかった（3分以上）
- ポートフォリオテンプレートのバリエーションが少ない

【バグ】
- 特になし

【その他コメント】
- 実際に役に立ちそう。実装したい。
```

#### 集計方法

| 項目 | ウェイト | 判定基準 |
|------|---------|---------|
| 満足度 | 30% | 4.0/5.0以上で OK |
| 実用性 | 30% | 3.5/5.0以上で OK |
| 改善要望 | 20% | 重大3件以上で対応 |
| バグ | 20% | 重大バグなしで OK |

### 2.3 修正 & 最適化

```
優先度 A（即座に対応）:
  └─ バグ・クリティカルなUX問題

優先度 B（段階1後に対応）:
  └─ 性能改善・機能追加

優先度 C（将来対応）:
  └─ 低優先度の改善
```

---

## 🚀 段階3: 段階1 リリース (Week 5-6)

### 3.1 本番環境への切り替え

#### 環境切り替えチェックリスト

```bash
# 1. 設定ファイル確認
[ ] config.json の environment が "production" に設定
[ ] .env ファイルが .gitignore に含まれている
[ ] ANTHROPIC_API_KEY が有効

# 2. ログ設定確認
[ ] LOG_LEVEL が INFO に設定
[ ] logs/ ディレクトリが作成可能
[ ] ログローテーション設定完了

# 3. キャッシュ確認
[ ] キャッシュディレクトリ (data/cache) が作成可能
[ ] キャッシュ TTL が適切に設定

# 4. 依存関係確認
[ ] 必要なライブラリがインストール済み
[ ] バージョン互換性確認

# 5. 本番 API キー設定
[ ] ANTHROPIC_API_KEY を本番キーに変更
[ ] API使用量制限が設定されている
```

#### デプロイメント実行

```bash
#!/bin/bash
# デプロイメントスクリプト

set -e  # エラー時に停止

echo "=== Pre-Deployment Checks ==="
# チェックリスト実行
bash scripts/pre_deployment_checks.sh

echo "=== Running Tests ==="
# テスト実行（すべてパスしることを確認）
bash tests/run_tests.sh

echo "=== Configuration Setup ==="
# 本番設定の適用
cp config.json.prod config.json

echo "=== Starting Agent ==="
# エージェント起動
python -m agents.main --config config.json

echo "=== Deployment Complete ==="
echo "Access URL: https://claude-code/agents/side-hustle-support"
```

### 3.2 初期ユーザー (20名) へのロールアウト

#### ユーザー招待

```
【招待メール テンプレート】

件名: 副業支援エージェントの提供開始

本文:
---
デジイナ大学メンバーの皆様へ

本日より、「副業支援エージェント」を提供開始いたします。

このエージェントは、皆様が副業で月5万円以上の収益化を
実現できるよう、以下をサポートします：

✅ スキルに最適な副業機会の発見
✅ ポートフォリオ・営業文の作成支援
✅ クライアント獲得戦略の提案
✅ 月次フォローアップ

【利用開始方法】
1. Claude Code を起動
2. メニューから「副業支援エージェント」を選択
3. 初回カウンセリングフォームを記入

【所要時間】
初回: 5～10分
継続: 2～5分/月

【質問・フィードバック】
#side-hustle-agent Slack チャネルで相談できます

皆様からのフィードバックをお待ちしています。

---
デジイナ大学運営チーム
```

#### 利用状況の監視

```
監視項目（毎日チェック）:
  - ユーザー数（登録、アクティブ）
  - エラー発生件数
  - API 使用量
  - 応答時間（平均、P95）

監視ツール:
  - ログファイル: logs/agent.log
  - ダッシュボード: Google Analytics（導入予定）
  - アラート: クリティカルエラー発生時
```

### 3.3 運用体制の整備

#### サポート体制

```
【サポート チャネル】

Slack: #side-hustle-agent
  ├─ ユーザー提案: 機能要望
  ├─ バグ報告: 問題報告
  └─ 雑談: 使用体験シェア

メール: support@dejiina-university.jp
  └─ 重大問題・緊急対応

【対応時間】
  平日 10:00-18:00 (24時間以内に回答目標)
```

#### 定期メンテナンス

```
【週次】
  - ログレビュー
  - エラーパターン分析
  - ユーザーフィードバック確認

【月次】
  - 使用統計レビュー
  - パフォーマンス分析
  - 改善提案の実装検討

【四半期ごと】
  - 大規模機能更新検討
  - セキュリティ監査
  - スケーリング計画
```

---

## 📈 段階4: 段階2・3への拡大 (Week 7+)

### 4.1 段階2: 100名への拡大

**条件**:
- 段階1の成功指標達成
  ✅ 満足度: 4.0/5.0以上
  ✅ エラー: 重大バグなし
  ✅ ユーザー評価: 正のコメント 80%以上

**スケジュール**:
```
Week 7-8: 段階1完全安定化
Week 9-10: 段階2へのロールアウト (50名追加)
Week 11-12: 完全展開 (100名達成)
```

### 4.2 段階3: フル公開

**条件**:
- 段階2の成功
- 月間 100名以上のアクティブユーザー

**公開範囲**:
- デジイナ大学全メンバー
- 外部向けデモンストレーション

---

## 🔄 継続的改善プロセス

### Workflow: 新機能リリース

```
ユーザーフィードバック
         ↓
ロードマップ更新
         ↓
機能設計 (1-2週間)
         ↓
実装 (2-3週間)
         ↓
テスト (1週間)
         ↓
ステージング検証
         ↓
段階的ロールアウト
         ↓
運用・改善
```

### バージョン管理

```
バージョン命名: v{major}.{minor}.{patch}

v1.0.0 (2026-07-XX): 初回リリース
  └─ コア機能完成

v1.1.0 (2026-08-XX): 機能追加フェーズ
  └─ ユーザーフィードバック反映

v1.2.0 (2026-09-XX): 最適化フェーズ
  └─ パフォーマンス改善、UX改善

v2.0.0 (2026-12-XX): メジャーアップグレード予定
  └─ 新機能の大型追加
```

---

## 🛡️ セキュリティ & コンプライアンス

### 1. データ保護

```
個人情報:
  ├─ ユーザー入力情報 → 暗号化して保存
  ├─ クライアント情報 → 最小限の保持
  └─ 使用統計 → 個人識別不可能に集計

データ保持期間:
  ├─ ユーザー入力: 1年間
  ├─ ログ: 30日間
  └─ キャッシュ: TTL による自動削除
```

### 2. アクセス制御

```
認証:
  ├─ デジイナ大学メンバー ID で認証
  └─ MFA（多要素認証）推奨（将来）

認可:
  ├─ アクティブメンバーのみアクセス可
  └─ 自分の情報のみ閲覧可
```

### 3. 監査ログ

```
記録対象:
  ├─ ユーザーログイン
  ├─ エージェント実行
  ├─ 生成された提案内容
  └─ エラー発生

ログ保持: 90日間
監査頻度: 月1回
```

---

## 📋 チェックリスト

### Go Live チェックリスト

```
[ ] ドキュメント完成
  [ ] AGENT_DEFINITION.md
  [ ] TOOL_INTEGRATION_SPEC.md
  [ ] WORKFLOW_DESIGN.md
  [ ] TEST_PLAN.md
  [ ] DEPLOYMENT_GUIDE.md
  [ ] README.md
  [ ] FAQ.md
  [ ] TROUBLESHOOTING.md

[ ] 環境構築
  [ ] config.json 準備
  [ ] .env ファイル設定
  [ ] ディレクトリ構造確認
  [ ] 依存関係インストール

[ ] テスト完了
  [ ] ユニットテスト: 100% PASS
  [ ] 統合テスト: 100% PASS
  [ ] ユーザビリティテスト: 満足度 4.0/5.0以上
  [ ] 性能テスト: 応答時間 OK

[ ] パイロット運用完了
  [ ] 5ユーザーによる検証
  [ ] フィードバック収集
  [ ] 重大バグ修正

[ ] 本番リリース準備
  [ ] 本番 API キー設定
  [ ] ログ設定確認
  [ ] バックアップ体制確認
  [ ] サポート体制整備
  [ ] ユーザー招待リスト準備

[ ] リリース実行
  [ ] デプロイメント実行
  [ ] 動作確認（smoke test）
  [ ] ユーザー招待送信
  [ ] 初日監視体制起動
```

---

## 📞 トラブルシューティング

### よくある問題

#### Q1: Web検索がタイムアウトしている
```
原因: ネットワーク遅延、検索キーワードが多すぎる
対応:
  1. キャッシュを確認: 過去のデータで対応するか
  2. キーワード数を減らす: 4個 → 3個に削減
  3. 一時的な問題の可能性: ユーザーに再試行を促す
```

#### Q2: Claude API のレート制限に達した
```
原因: 予想以上にユーザーが多い
対応:
  1. 即座: 低優先度タスクをキューイング
  2. 翌日: トークンバジェットを見直し
  3. 長期: API呼び出しの最適化を実施
```

#### Q3: エージェントが起動しない
```
原因: config.json エラー、API キー無効
対応:
  1. config.json の構文確認: `python -m json.tool config.json`
  2. API キーの確認: 環境変数を確認
  3. ログファイルを確認: `tail -f logs/agent.log`
```

詳細は [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) 参照

---

## 🎓 その他のリソース

- [運用ガイド](./OPERATIONAL_GUIDE.md): 日々の運用手順
- [FAQ](./FAQ.md): ユーザーからのよくある質問
- [プロダクトロードマップ](./ROADMAP.md): 今後の機能計画

---

**バージョン**: 1.0  
**最終更新**: 2026-06-20  
**ステータス**: 実装前 → Go Live準備中
