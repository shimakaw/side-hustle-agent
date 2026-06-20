"""
統合テスト
複数のモジュールが正しく連動するかテスト
"""

import unittest
import sys
import os

# パスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from agents.profiler import UserProfile, UserProfiler, ExperienceLevel, TimeCommitment
from agents.keyword_generator import KeywordGenerator
from agents.analyzer import SideHustleAnalyzer
from agents.search_engine import SearchEngine
from agents.web_fetch import WebFetcher, PlatformType
from agents.cache_manager import CacheManager
from agents.trust_scorer import TrustScorer
from agents.template_generator import TemplateGenerator
from agents.main import SideHustleSupportAgent


class TestWorkflowIntegration(unittest.TestCase):
    """ワークフロー統合テスト"""

    def setUp(self):
        """テストの初期化"""
        self.profiler = UserProfiler()
        self.keyword_generator = KeywordGenerator()
        self.analyzer = SideHustleAnalyzer()

    def test_profile_to_keywords_to_opportunities(self):
        """プロフィール → キーワード生成 → 機会分析"""

        # 1. プロフィール作成
        success, profile = self.profiler.create_profile(
            name="テストユーザー",
            experience_level=ExperienceLevel.INTERMEDIATE,
            skills=["python", "data analysis"],
            target_monthly_income=100000,
            time_commitment=TimeCommitment.SEMI_FULL_TIME
        )

        self.assertTrue(success)
        self.assertIsInstance(profile, UserProfile)

        # 2. キーワード生成
        keywords = self.keyword_generator.generate_keywords(profile, count=6)

        self.assertEqual(len(keywords), 6)
        self.assertTrue(all(isinstance(k, str) for k in keywords))

        # 3. 副業機会分析
        opportunities = self.analyzer.find_opportunities(profile, top_n=3)

        self.assertEqual(len(opportunities), 3)
        self.assertTrue(all(opp.match_score > 0 for opp in opportunities))

    def test_search_and_trust_scoring(self):
        """Web検索 → 信頼度スコアリング"""

        search_engine = SearchEngine(enable_mock=True)
        trust_scorer = TrustScorer()

        # 1. Web検索
        success, results = search_engine.search(
            ["python freelance", "data analysis"],
            max_results=5
        )

        self.assertTrue(success)
        self.assertGreater(len(results), 0)

        # 2. 信頼度スコアリング
        scored_results = trust_scorer.compare_search_results(
            [{"source": r.source, "url": r.url, "snippet": r.snippet}
             for r in results]
        )

        self.assertEqual(len(scored_results), len(results))
        self.assertTrue(all(0 <= r['trust_score'] <= 100 for r in scored_results))

    def test_platform_analysis_workflow(self):
        """プラットフォーム分析ワークフロー"""

        web_fetcher = WebFetcher(enable_mock=True)

        # 1. 複数プラットフォームのデータ取得
        platforms = [PlatformType.UPWORK, PlatformType.FIVERR, PlatformType.COCONALA]
        platform_data = web_fetcher.fetch_multiple_platforms(platforms)

        self.assertEqual(len(platform_data), 3)

        # 2. プラットフォーム比較
        comparison = web_fetcher.compare_platforms(platforms)

        self.assertIn("best_hourly_rate", comparison)
        self.assertIn("best_success_rate", comparison)
        self.assertIn("highest_demand", comparison)

    def test_template_generation_workflow(self):
        """テンプレート生成ワークフロー"""

        profiler = UserProfiler()
        template_gen = TemplateGenerator(use_mock=True)

        # 1. プロフィール作成
        success, profile = profiler.create_profile(
            name="テンプレートテスト",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["writing", "social media"],
            target_monthly_income=50000,
            time_commitment=TimeCommitment.PART_TIME
        )

        self.assertTrue(success)

        # 2. ポートフォリオテンプレート生成
        portfolio = template_gen.generate_portfolio_template(profile, "upwork")
        self.assertIsNotNone(portfolio.content)
        self.assertIn(profile.name, portfolio.content)

        # 3. 営業メール生成
        email = template_gen.generate_sales_email(profile)
        self.assertIsNotNone(email.content)
        self.assertIn("件名", email.content)

        # 4. SNS投稿生成
        sns = template_gen.generate_sns_posts(profile)
        self.assertEqual(len(sns), 3)
        self.assertIn("twitter", sns)
        self.assertIn("instagram", sns)
        self.assertIn("linkedin", sns)

    def test_cache_workflow(self):
        """キャッシュワークフロー"""

        cache = CacheManager()
        search_engine = SearchEngine(enable_mock=True)

        # 1. Web検索実行
        success, results = search_engine.search(["python"], max_results=5)
        self.assertTrue(success)

        # 2. 結果をキャッシュに保存
        cache_key = "python_search_results"
        cache.set(cache_key, results, ttl_hours=24)

        # 3. キャッシュから取得
        cached_results = cache.get(cache_key)
        self.assertIsNotNone(cached_results)
        self.assertEqual(len(cached_results), len(results))

        # 4. キャッシュ統計確認
        stats = cache.get_stats()
        self.assertGreater(stats['valid_entries'], 0)


class TestMainAgentIntegration(unittest.TestCase):
    """メインエージェント統合テスト"""

    def setUp(self):
        """テストの初期化"""
        self.agent = SideHustleSupportAgent()

    def test_initial_counseling_flow(self):
        """初回カウンセリングフロー"""

        success, result = self.agent.initial_counseling(
            name="統合テストユーザー",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["python", "web development"],
            target_monthly_income=75000,
            time_commitment=TimeCommitment.PART_TIME
        )

        self.assertTrue(success)
        self.assertIn("profile", result)
        self.assertIn("keywords", result)
        self.assertIn("opportunities", result)

        # プロフィール確認
        profile = result['profile']
        self.assertEqual(profile['name'], "統合テストユーザー")
        self.assertEqual(profile['target_monthly_income'], 75000)

    def test_full_session_workflow(self):
        """フルセッションワークフロー"""

        results = self.agent.run_full_session(
            name="フルセッションテスト",
            experience_level=ExperienceLevel.INTERMEDIATE,
            skills=["data analysis", "python"],
            target_monthly_income=100000,
            time_commitment=TimeCommitment.SEMI_FULL_TIME
        )

        # すべての結果が含まれているか確認
        self.assertIn("counseling", results)
        self.assertIn("templates", results)
        self.assertIn("platform_analysis", results)
        self.assertIn("roadmap", results)

        # カウンセリング結果確認
        self.assertIn("profile", results['counseling'])
        self.assertIn("opportunities", results['counseling'])

        # テンプレート結果確認
        templates = results['templates']
        self.assertIn("portfolio", templates)
        self.assertIn("sales", templates)
        self.assertIn("sns", templates)

    def test_agent_state_management(self):
        """エージェントの状態管理"""

        # ユーザーが設定されていない状態
        self.assertIsNone(self.agent.current_user)

        # 初回カウンセリング実行
        self.agent.initial_counseling(
            name="状態管理テスト",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["writing"],
            target_monthly_income=50000,
            time_commitment=TimeCommitment.PART_TIME
        )

        # ユーザーが設定されているか確認
        self.assertIsNotNone(self.agent.current_user)
        self.assertEqual(self.agent.current_user.name, "状態管理テスト")

    def test_cache_integration(self):
        """キャッシュ統合テスト"""

        # フルセッション実行
        self.agent.run_full_session(
            name="キャッシュテスト",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["python"],
            target_monthly_income=50000,
            time_commitment=TimeCommitment.PART_TIME
        )

        # キャッシュ統計確認
        cache_stats = self.agent.get_cache_stats()
        self.assertIsInstance(cache_stats, dict)
        self.assertIn("valid_entries", cache_stats)
        self.assertIn("cache_dir", cache_stats)


class TestErrorHandling(unittest.TestCase):
    """エラーハンドリングテスト"""

    def test_invalid_profile_handling(self):
        """無効なプロフィールハンドリング"""

        profiler = UserProfiler()

        # 無効なデータ
        success, result = profiler.create_profile(
            name="",  # 無効な名前
            experience_level=ExperienceLevel.BEGINNER,
            skills=[],  # スキルなし
            target_monthly_income=1000,  # 最小値より低い
            time_commitment=TimeCommitment.PART_TIME
        )

        self.assertFalse(success)
        self.assertIsInstance(result, str)

    def test_empty_search_results_handling(self):
        """空の検索結果ハンドリング"""

        search_engine = SearchEngine(enable_mock=True)

        # 空のキーワード
        success, results = search_engine.search([], max_results=5)

        self.assertFalse(success)
        self.assertEqual(len(results), 0)

    def test_template_without_profile(self):
        """プロフィール無しのテンプレート生成"""

        agent = SideHustleSupportAgent()

        # プロフィール設定なしでテンプレート生成
        result = agent.generate_all_templates()

        self.assertIn("error", result)

    def test_roadmap_without_profile(self):
        """プロフィール無しのロードマップ生成"""

        agent = SideHustleSupportAgent()

        # プロフィール設定なしでロードマップ生成
        result = agent.generate_roadmap()

        self.assertIn("error", result)


class TestPerformance(unittest.TestCase):
    """パフォーマンステスト"""

    def test_keyword_generation_performance(self):
        """キーワード生成のパフォーマンス"""

        import time

        profiler = UserProfiler()
        keyword_gen = KeywordGenerator()

        # プロフィール作成
        _, profile = profiler.create_profile(
            name="パフォーマンステスト",
            experience_level=ExperienceLevel.INTERMEDIATE,
            skills=["python", "javascript", "data analysis", "web development"],
            target_monthly_income=100000,
            time_commitment=TimeCommitment.SEMI_FULL_TIME
        )

        # キーワード生成時間測定
        start = time.time()
        keywords = keyword_gen.generate_keywords(profile, count=6)
        elapsed = time.time() - start

        # 1秒以内に完了するはず
        self.assertLess(elapsed, 1.0)
        self.assertEqual(len(keywords), 6)

    def test_template_generation_performance(self):
        """テンプレート生成のパフォーマンス"""

        import time

        profiler = UserProfiler()
        template_gen = TemplateGenerator(use_mock=True)

        _, profile = profiler.create_profile(
            name="テンプレートパフォーマンステスト",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["writing"],
            target_monthly_income=50000,
            time_commitment=TimeCommitment.PART_TIME
        )

        # テンプレート生成時間測定
        start = time.time()
        sns_templates = template_gen.generate_sns_posts(profile)
        elapsed = time.time() - start

        # 1秒以内に完了するはず
        self.assertLess(elapsed, 1.0)
        self.assertEqual(len(sns_templates), 3)


if __name__ == '__main__':
    unittest.main()
