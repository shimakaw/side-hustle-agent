#!/usr/bin/env python3
"""
副業支援エージェント デモンストレーション
"""

import sys
import os

# パスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.main import SideHustleSupportAgent
from agents.profiler import ExperienceLevel, TimeCommitment
import json


def print_section(title: str):
    """セクションヘッダーを表示"""
    print(f"\n{'='*60}")
    print(f"📌 {title}")
    print(f"{'='*60}\n")


def demo_basic_workflow():
    """基本的なワークフローのデモ"""

    print_section("副業支援エージェント デモンストレーション")

    # エージェントを初期化
    agent = SideHustleSupportAgent()

    print("✨ エージェントを初期化しました\n")

    # サンプルユーザー情報
    sample_user = {
        "name": "山田太郎",
        "experience_level": ExperienceLevel.BEGINNER,
        "skills": ["python", "data analysis", "writing"],
        "target_monthly_income": 50000,
        "time_commitment": TimeCommitment.PART_TIME
    }

    print("📋 サンプルユーザー情報:")
    print(f"  名前: {sample_user['name']}")
    print(f"  経験: {sample_user['experience_level'].value}")
    print(f"  スキル: {', '.join(sample_user['skills'])}")
    print(f"  目標月収: ¥{sample_user['target_monthly_income']:,}")
    print(f"  時間的余裕: {sample_user['time_commitment'].value}\n")

    # フルセッション実行
    results = agent.run_full_session(**sample_user)

    # 結果を表示
    print_section("🎯 初回カウンセリング結果")

    counseling = results.get("counseling", {})
    if "error" not in counseling:
        print(f"✅ プロフィール作成成功")
        print(f"  名前: {counseling['profile']['name']}")
        print(f"  スキル: {', '.join(counseling['profile']['skills'])}")
        print(f"\n🔑 生成されたキーワード:")
        for i, keyword in enumerate(counseling['keywords'], 1):
            print(f"  {i}. {keyword}")
        print(f"\n📊 検索結果:")
        print(f"  取得件数: {counseling['search_results_count']}")
        print(f"  信頼度高い結果: {counseling['trusted_results']}")
        print(f"\n💼 推奨される副業機会（TOP 3）:")
        for i, opp in enumerate(counseling['opportunities'], 1):
            print(f"  {i}. {opp['title']}")
            print(f"     マッチスコア: {opp['match_score']}%")
            print(f"     予想月収: ¥{opp['estimated_income']:,}\n")

    # テンプレート生成結果
    print_section("📝 生成されたテンプレート")

    templates = results.get("templates", {})
    print("✅ ポートフォリオテンプレート:")
    for platform, data in templates.get("portfolio", {}).items():
        print(f"  • {platform}: {data['full_length']}文字")

    print("\n✅ 営業メールテンプレート:")
    for platform, data in templates.get("sales", {}).items():
        print(f"  • {platform}: {data['full_length']}文字")

    print("\n✅ SNS投稿テンプレート:")
    for platform, data in templates.get("sns", {}).items():
        print(f"  • {platform}: {data['full_length']}文字")

    # プラットフォーム分析
    print_section("🌐 プラットフォーム分析")

    platform_data = results.get("platform_analysis", {})
    comparison = platform_data.get("comparison", {})

    if "best_hourly_rate" in comparison:
        print(f"⭐ 最高時給: {comparison['best_hourly_rate']}")
        print(f"⭐ 成功率最高: {comparison['best_success_rate']}")
        print(f"⭐ 高需要プラットフォーム: {', '.join(comparison['highest_demand'])}")

    # ロードマップ
    print_section("🗺️  副業ロードマップ")

    roadmap = results.get("roadmap", {}).get("roadmap", {})

    if "opportunity" in roadmap:
        print(f"🎯 推奨副業: {roadmap['opportunity']['title']}")
        print(f"   マッチスコア: {roadmap['opportunity']['match_score']}%")

        phases = roadmap.get("phases", {})
        print(f"\n📅 実行フェーズ:")
        for phase_name, phase_data in phases.items():
            print(f"  【{phase_name}】 ({phase_data['duration_weeks']}週間)")
            for task in phase_data['tasks']:
                print(f"    ✓ {task}")

        print(f"\n💰 収入予測:")
        income = roadmap.get("income_projection", {})
        print(f"  2週目: ¥{income.get('week_2', 0):,}")
        print(f"  4週目: ¥{income.get('week_4', 0):,}")
        print(f"  3ヶ月目: ¥{income.get('month_3', 0):,}")

    # キャッシュ統計
    print_section("💾 キャッシュ統計")

    cache_stats = agent.get_cache_stats()
    print(f"  有効エントリ: {cache_stats['valid_entries']}")
    print(f"  期限切れエントリ: {cache_stats['expired_entries']}")
    print(f"  合計サイズ: {cache_stats['total_size_bytes']} bytes")

    # 検索履歴
    print_section("🔍 検索履歴")

    search_history = agent.get_search_history()
    if search_history:
        for i, search in enumerate(search_history[:3], 1):
            print(f"  {i}. クエリ: {search['query']}")
            print(f"     結果数: {search['result_count']}\n")

    print("=" * 60)
    print("✅ デモンストレーション完了！")
    print("=" * 60 + "\n")


def demo_individual_features():
    """個別機能のデモ"""

    print_section("個別機能デモンストレーション")

    agent = SideHustleSupportAgent()

    # 1. プロファイリングのデモ
    print("1️⃣  プロファイリング機能")
    success, profile = agent.profiler.create_profile(
        name="テストユーザー",
        experience_level=ExperienceLevel.INTERMEDIATE,
        skills=["web development", "ui design"],
        target_monthly_income=100000,
        time_commitment=TimeCommitment.SEMI_FULL_TIME
    )
    print(f"   ✅ プロフィール作成: {'成功' if success else '失敗'}\n")

    # 2. キーワード生成のデモ
    if success:
        print("2️⃣  キーワード生成")
        keywords = agent.keyword_generator.generate_keywords(profile, count=6)
        print(f"   生成キーワード: {', '.join(keywords)}\n")

    # 3. 副業分析のデモ
    print("3️⃣  副業機会分析")
    opportunities = agent.analyzer.find_opportunities(profile, top_n=3)
    for opp in opportunities:
        print(f"   • {opp.title} (スコア: {opp.match_score}%)")
    print()

    # 4. Web検索のデモ
    print("4️⃣  Web検索")
    search_success, results = agent.search_engine.search(
        ["web development freelance", "ui design jobs"],
        max_results=5
    )
    print(f"   検索結果: {len(results)}件\n")

    # 5. プラットフォーム分析のデモ
    print("5️⃣  プラットフォーム分析")
    from agents.web_fetch import PlatformType
    comparison = agent.web_fetcher.compare_platforms(
        [PlatformType.UPWORK, PlatformType.FIVERR, PlatformType.COCONALA]
    )
    print(f"   最高時給プラットフォーム: {comparison.get('best_hourly_rate', 'N/A')}")
    print(f"   高需要: {', '.join(comparison.get('highest_demand', []))}\n")

    print("✅ すべての機能デモ完了！\n")


if __name__ == "__main__":
    try:
        # メインデモ
        demo_basic_workflow()

        # 個別機能デモ
        demo_individual_features()

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
