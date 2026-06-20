"""
副業支援エージェント メインクラス
すべてのモジュールを統合
"""

from typing import Dict, Optional, List, Tuple
import json
from .profiler import UserProfile, UserProfiler, ExperienceLevel, TimeCommitment
from .file_handler import FileHandler
from .keyword_generator import KeywordGenerator
from .analyzer import SideHustleAnalyzer
from .search_engine import SearchEngine
from .web_fetch import WebFetcher, PlatformType
from .cache_manager import CacheManager
from .trust_scorer import TrustScorer
from .template_generator import TemplateGenerator


class SideHustleSupportAgent:
    """副業支援エージェント"""

    def __init__(self, config_path: str = "config.json"):
        """
        Args:
            config_path: 設定ファイルのパス
        """
        self.config = self._load_config(config_path)

        # モジュールを初期化
        self.profiler = UserProfiler()
        self.file_handler = FileHandler()
        self.keyword_generator = KeywordGenerator()
        self.analyzer = SideHustleAnalyzer()
        self.search_engine = SearchEngine(enable_mock=True)
        self.web_fetcher = WebFetcher(enable_mock=True)
        self.cache_manager = CacheManager()
        self.trust_scorer = TrustScorer()
        self.template_generator = TemplateGenerator(use_mock=True)

        self.current_user: Optional[UserProfile] = None

    def _load_config(self, config_path: str) -> Dict:
        """設定ファイルを読み込む"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"設定読み込みエラー: {e}")
            return {}

    # ========================
    # ステップ 1: 初回カウンセリング
    # ========================

    def initial_counseling(self,
                          name: str,
                          experience_level: ExperienceLevel,
                          skills: List[str],
                          target_monthly_income: int,
                          time_commitment: TimeCommitment) -> Tuple[bool, Dict]:
        """初回カウンセリング"""

        print("=" * 50)
        print("🎯 初回カウンセリング開始")
        print("=" * 50)

        # ステップ 1: プロフィール作成
        success, result = self.profiler.create_profile(
            name=name,
            experience_level=experience_level,
            skills=skills,
            target_monthly_income=target_monthly_income,
            time_commitment=time_commitment
        )

        if not success:
            return False, {"error": result}

        self.current_user = result

        # ステップ 2: キーワード生成
        keywords = self.keyword_generator.generate_keywords(self.current_user, count=6)

        # ステップ 3: Web検索
        search_success, search_results = self.search_engine.search(keywords, max_results=10)

        # ステップ 4: 信頼度スコアリング
        scored_results = self.trust_scorer.compare_search_results(
            [{"source": r.source, "url": r.url, "snippet": r.snippet}
             for r in search_results]
        )

        # ステップ 5: 副業機会の分析
        opportunities = self.analyzer.find_opportunities(self.current_user, top_n=3)

        return True, {
            "profile": self.current_user.to_dict(),
            "keywords": keywords,
            "search_results_count": len(search_results),
            "trusted_results": len([r for r in scored_results if r['trust_score'] >= 60]),
            "opportunities": [
                {
                    "title": opp.title,
                    "description": opp.description,
                    "match_score": opp.match_score,
                    "estimated_income": opp.estimated_monthly_income
                }
                for opp in opportunities
            ]
        }

    # ========================
    # ステップ 2: テンプレート生成
    # ========================

    def generate_all_templates(self) -> Dict:
        """すべてのテンプレートを生成"""

        if not self.current_user:
            return {"error": "プロフィールが設定されていません"}

        print("=" * 50)
        print("📝 テンプレート生成開始")
        print("=" * 50)

        results = {
            "portfolio": {},
            "sales": {},
            "sns": {}
        }

        # ポートフォリオテンプレート
        for platform in ["upwork", "fiverr", "coconala"]:
            template = self.template_generator.generate_portfolio_template(
                self.current_user,
                platform=platform
            )
            results["portfolio"][platform] = {
                "content": template.content[:200] + "...",  # 先頭200文字
                "full_length": len(template.content)
            }

        # 営業メール
        email_template = self.template_generator.generate_sales_email(self.current_user)
        results["sales"]["email"] = {
            "content": email_template.content[:200] + "...",
            "full_length": len(email_template.content)
        }

        # SNS投稿
        sns_templates = self.template_generator.generate_sns_posts(self.current_user)
        for platform, template in sns_templates.items():
            results["sns"][platform] = {
                "content": template.content[:200] + "...",
                "full_length": len(template.content)
            }

        return results

    # ========================
    # ステップ 3: プラットフォーム分析
    # ========================

    def analyze_platforms(self) -> Dict:
        """プラットフォーム分析"""

        print("=" * 50)
        print("🌐 プラットフォーム分析")
        print("=" * 50)

        platforms = [PlatformType.UPWORK, PlatformType.FIVERR, PlatformType.COCONALA]
        comparison = self.web_fetcher.compare_platforms(platforms)

        if not self.current_user:
            return {"error": "プロフィールが設定されていません"}

        recommendation = self.web_fetcher.get_recommendation(
            self.current_user.skills,
            platforms=platforms
        )

        return {
            "comparison": comparison,
            "recommendation": recommendation
        }

    # ========================
    # ステップ 4: ロードマップ生成
    # ========================

    def generate_roadmap(self) -> Dict:
        """副業ロードマップを生成"""

        if not self.current_user:
            return {"error": "プロフィールが設定されていません"}

        print("=" * 50)
        print("🗺️  副業ロードマップ生成")
        print("=" * 50)

        roadmap = self.analyzer.get_roadmap(self.current_user)
        skill_gap = self.analyzer.get_skill_gap_analysis(self.current_user)

        return {
            "roadmap": roadmap,
            "skill_gap_analysis": skill_gap
        }

    # ========================
    # 統合実行
    # ========================

    def run_full_session(self,
                        name: str,
                        experience_level: ExperienceLevel,
                        skills: List[str],
                        target_monthly_income: int,
                        time_commitment: TimeCommitment) -> Dict:
        """フルセッション実行（初回〜テンプレート生成）"""

        print("\n" + "=" * 60)
        print("🚀 副業支援エージェント フルセッション開始")
        print("=" * 60 + "\n")

        session_results = {}

        # 1. 初回カウンセリング
        counseling_success, counseling_result = self.initial_counseling(
            name, experience_level, skills, target_monthly_income, time_commitment
        )
        session_results["counseling"] = counseling_result

        if not counseling_success:
            return session_results

        # 2. テンプレート生成
        session_results["templates"] = self.generate_all_templates()

        # 3. プラットフォーム分析
        session_results["platform_analysis"] = self.analyze_platforms()

        # 4. ロードマップ生成
        session_results["roadmap"] = self.generate_roadmap()

        print("\n" + "=" * 60)
        print("✅ フルセッション完了！")
        print("=" * 60 + "\n")

        return session_results

    # ========================
    # ユーティリティ
    # ========================

    def get_cache_stats(self) -> Dict:
        """キャッシュ統計を取得"""
        return self.cache_manager.get_stats()

    def get_search_history(self) -> List:
        """検索履歴を取得"""
        return self.search_engine.get_search_history()

    def export_session_results(self, filepath: str) -> bool:
        """セッション結果をエクスポート"""
        try:
            if not self.current_user:
                return False

            results = {
                "user": self.current_user.to_dict(),
                "templates": self.template_generator.get_all_generated_templates(),
                "cache_stats": self.cache_manager.get_stats(),
                "search_history": self.search_engine.get_search_history()
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"エクスポートエラー: {e}")
            return False
