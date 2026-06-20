"""
WebFetch モジュール
ウェブサイトからデータを抽出
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class PlatformType(Enum):
    """プラットフォームタイプ"""
    UPWORK = "upwork"
    FIVERR = "fiverr"
    COCONALA = "coconala"
    CROWDWORKS = "crowdworks"
    LANCERS = "lancers"


@dataclass
class PlatformData:
    """プラットフォームデータ"""
    platform: PlatformType
    average_hourly_rate: float
    average_project_rate: float
    demand_level: str  # low, medium, high
    competition_level: str  # low, medium, high
    popular_categories: List[str]
    success_rate: float  # 0-1


class WebFetcher:
    """ウェブサイトからのデータ抽出"""

    # プラットフォーム別の模擬データ
    PLATFORM_DATA = {
        PlatformType.UPWORK: {
            "average_hourly_rate": 50,
            "average_project_rate": 500,
            "demand_level": "high",
            "competition_level": "high",
            "popular_categories": [
                "Web Development",
                "Graphic Design",
                "Data Analysis",
                "Writing"
            ],
            "success_rate": 0.75
        },
        PlatformType.FIVERR: {
            "average_hourly_rate": 15,
            "average_project_rate": 50,
            "demand_level": "high",
            "competition_level": "very_high",
            "popular_categories": [
                "Graphics & Design",
                "Writing",
                "Video & Animation",
                "Music & Audio"
            ],
            "success_rate": 0.50
        },
        PlatformType.COCONALA: {
            "average_hourly_rate": 30,
            "average_project_rate": 300,
            "demand_level": "medium",
            "competition_level": "medium",
            "popular_categories": [
                "プログラミング",
                "ライティング",
                "デザイン",
                "マーケティング"
            ],
            "success_rate": 0.65
        },
        PlatformType.CROWDWORKS: {
            "average_hourly_rate": 25,
            "average_project_rate": 250,
            "demand_level": "medium",
            "competition_level": "medium",
            "popular_categories": [
                "プログラミング",
                "データ入力",
                "ライティング",
                "デザイン"
            ],
            "success_rate": 0.60
        },
        PlatformType.LANCERS: {
            "average_hourly_rate": 28,
            "average_project_rate": 280,
            "demand_level": "medium",
            "competition_level": "medium",
            "popular_categories": [
                "プログラミング",
                "ライティング",
                "デザイン",
                "翻訳"
            ],
            "success_rate": 0.62
        }
    }

    def __init__(self, enable_mock: bool = True):
        self.enable_mock = enable_mock
        self.fetch_cache: Dict[str, PlatformData] = {}

    def fetch_platform_data(self, platform: PlatformType) -> Optional[PlatformData]:
        """プラットフォームデータを取得"""

        # キャッシュをチェック
        if platform.value in self.fetch_cache:
            return self.fetch_cache[platform.value]

        try:
            if self.enable_mock:
                data = self._fetch_mock(platform)
            else:
                data = self._fetch_real(platform)

            if data:
                self.fetch_cache[platform.value] = data

            return data

        except Exception as e:
            print(f"フェッチエラー ({platform.value}): {e}")
            return None

    def _fetch_mock(self, platform: PlatformType) -> Optional[PlatformData]:
        """模擬データを取得"""

        if platform not in self.PLATFORM_DATA:
            return None

        data = self.PLATFORM_DATA[platform]

        return PlatformData(
            platform=platform,
            average_hourly_rate=data['average_hourly_rate'],
            average_project_rate=data['average_project_rate'],
            demand_level=data['demand_level'],
            competition_level=data['competition_level'],
            popular_categories=data['popular_categories'],
            success_rate=data['success_rate']
        )

    def _fetch_real(self, platform: PlatformType) -> Optional[PlatformData]:
        """実際のサイトからのフェッチ（実装時）"""
        # TODO: BeautifulSoup, Selenium などで実装
        return self._fetch_mock(platform)

    def fetch_multiple_platforms(self,
                                platforms: List[PlatformType]) -> Dict[str, PlatformData]:
        """複数プラットフォームのデータを取得"""

        results = {}
        for platform in platforms:
            data = self.fetch_platform_data(platform)
            if data:
                results[platform.value] = data

        return results

    def compare_platforms(self,
                         platforms: List[PlatformType]) -> Dict:
        """プラットフォーム比較"""

        platform_data = self.fetch_multiple_platforms(platforms)

        if not platform_data:
            return {}

        # 平均時給で比較
        hourly_rates = {
            name: data.average_hourly_rate
            for name, data in platform_data.items()
        }

        # 成功率で比較
        success_rates = {
            name: data.success_rate
            for name, data in platform_data.items()
        }

        # 需要レベルで比較
        demand_levels = {
            name: data.demand_level
            for name, data in platform_data.items()
        }

        return {
            "hourly_rates": hourly_rates,
            "success_rates": success_rates,
            "demand_levels": demand_levels,
            "best_hourly_rate": max(hourly_rates, key=hourly_rates.get),
            "best_success_rate": max(success_rates, key=success_rates.get),
            "highest_demand": [
                name for name, level in demand_levels.items()
                if level == "high"
            ]
        }

    def get_cache_info(self) -> Dict:
        """キャッシュ情報を取得"""
        return {
            "cached_platforms": list(self.fetch_cache.keys()),
            "cache_size": len(self.fetch_cache)
        }

    def clear_cache(self, platform: Optional[PlatformType] = None) -> bool:
        """キャッシュをクリア"""
        if platform:
            if platform.value in self.fetch_cache:
                del self.fetch_cache[platform.value]
                return True
            return False
        else:
            self.fetch_cache.clear()
            return True

    def get_recommendation(self,
                          skills: List[str],
                          platforms: Optional[List[PlatformType]] = None) -> Dict:
        """スキルに基づく推奨プラットフォーム"""

        if not platforms:
            platforms = list(PlatformType)

        platform_data = self.fetch_multiple_platforms(platforms)

        if not platform_data:
            return {}

        # スコアリング（需要、成功率、競争度）
        scores = {}
        for platform_name, data in platform_data.items():
            demand_score = {"low": 1, "medium": 2, "high": 3}.get(data.demand_level, 2)
            competition_score = {"low": 3, "medium": 2, "high": 1, "very_high": 0}.get(
                data.competition_level, 1
            )
            success_score = data.success_rate * 3

            total_score = (demand_score * 0.3 + competition_score * 0.3 + success_score * 0.4)
            scores[platform_name] = round(total_score, 2)

        # スコアでソート
        sorted_platforms = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return {
            "scores": scores,
            "recommendation": [
                {
                    "rank": i + 1,
                    "platform": platform_name,
                    "score": score,
                    "reason": self._get_recommendation_reason(platform_name, platform_data)
                }
                for i, (platform_name, score) in enumerate(sorted_platforms[:3])
            ]
        }

    def _get_recommendation_reason(self, platform_name: str, platform_data: Dict) -> str:
        """推奨理由を生成"""
        data = platform_data.get(platform_name)
        if not data:
            return ""

        if data.success_rate > 0.7:
            return f"高い成功率 ({data.success_rate*100:.0f}%)"
        elif data.demand_level == "high":
            return "需要が高い"
        else:
            return f"競争が少なく、単価が ${data.average_hourly_rate:.0f}/時間"
