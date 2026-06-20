"""
信頼度スコアリングモジュール
検索結果やデータの信頼度を評価
"""

from typing import List, Dict, Tuple
from enum import Enum


class TrustLevel(Enum):
    """信頼度レベル"""
    VERY_LOW = "very_low"  # 0-20
    LOW = "low"  # 20-40
    MEDIUM = "medium"  # 40-60
    HIGH = "high"  # 60-80
    VERY_HIGH = "very_high"  # 80-100


class TrustScorer:
    """信頼度スコアリング"""

    # ソース別の基本信頼度スコア
    SOURCE_SCORES = {
        "upwork": 85,
        "fiverr": 75,
        "coconala": 70,
        "crowdworks": 70,
        "lancers": 70,
        "official_blog": 90,
        "news_site": 80,
        "forum": 50,
        "social_media": 40,
        "unknown": 30
    }

    # ドメイン別の基本信頼度スコア
    DOMAIN_SCORES = {
        ".com": 75,
        ".org": 80,
        ".gov": 95,
        ".edu": 90,
        ".jp": 75,
        ".co.jp": 80,
        "upwork.com": 90,
        "fiverr.com": 85,
        "github.com": 85
    }

    def __init__(self):
        pass

    def calculate_source_score(self, source: str) -> float:
        """ソースの信頼度スコアを計算"""
        source_lower = source.lower()

        # 完全一致
        if source_lower in self.SOURCE_SCORES:
            return float(self.SOURCE_SCORES[source_lower])

        # 部分一致
        for known_source, score in self.SOURCE_SCORES.items():
            if known_source in source_lower:
                return float(score)

        # デフォルト
        return 30.0

    def calculate_url_score(self, url: str) -> float:
        """URL の信頼度スコアを計算"""
        url_lower = url.lower()
        score = 50.0

        # ドメイン別スコア
        for domain, domain_score in self.DOMAIN_SCORES.items():
            if domain in url_lower:
                score = float(domain_score)
                break

        # HTTPS の場合はボーナス
        if url.startswith("https://"):
            score += 5

        return min(score, 100.0)

    def calculate_content_score(self, content: str) -> float:
        """コンテンツ品質スコアを計算"""
        score = 50.0

        # 長さをチェック（コンテンツが充実しているか）
        if len(content) > 200:
            score += 10
        if len(content) > 500:
            score += 10

        # 具体的な数字が含まれているか
        if any(char.isdigit() for char in content):
            score += 5

        # 更新日が明記されているか
        if any(year in content for year in ["2024", "2023", "2022"]):
            score += 10

        return min(score, 100.0)

    def calculate_overall_score(self,
                               source: str = "unknown",
                               url: str = "",
                               content: str = "") -> Tuple[float, TrustLevel]:
        """総合信頼度スコアを計算"""

        source_score = self.calculate_source_score(source)
        url_score = self.calculate_url_score(url)
        content_score = self.calculate_content_score(content)

        # 重み付け平均
        overall_score = (
            source_score * 0.5 +
            url_score * 0.3 +
            content_score * 0.2
        )

        overall_score = min(max(overall_score, 0.0), 100.0)

        # 信頼度レベルを決定
        trust_level = self._score_to_level(overall_score)

        return round(overall_score, 1), trust_level

    def _score_to_level(self, score: float) -> TrustLevel:
        """スコアを信頼度レベルに変換"""
        if score < 20:
            return TrustLevel.VERY_LOW
        elif score < 40:
            return TrustLevel.LOW
        elif score < 60:
            return TrustLevel.MEDIUM
        elif score < 80:
            return TrustLevel.HIGH
        else:
            return TrustLevel.VERY_HIGH

    def rate_sources(self, sources: List[str]) -> List[Dict]:
        """複数のソースを評価"""
        ratings = []

        for source in sources:
            score = self.calculate_source_score(source)
            level = self._score_to_level(score)

            ratings.append({
                "source": source,
                "score": score,
                "level": level.value,
                "recommendation": self._get_recommendation(score)
            })

        # スコアで降順ソート
        return sorted(ratings, key=lambda x: x['score'], reverse=True)

    def _get_recommendation(self, score: float) -> str:
        """信頼度スコアに基づく推奨"""
        if score >= 80:
            return "非常に信頼できる。積極的に参考にしても良い"
        elif score >= 60:
            return "比較的信頼できる。参考にしても良いが、複数の情報と確認"
        elif score >= 40:
            return "ある程度参考にできるが、他の信頼できる情報と比較推奨"
        else:
            return "信頼度が低い。複数の信頼できる情報で検証が必要"

    def compare_search_results(self, results: List[Dict]) -> List[Dict]:
        """複数の検索結果を信頼度で比較"""
        scored_results = []

        for result in results:
            score, level = self.calculate_overall_score(
                source=result.get('source', 'unknown'),
                url=result.get('url', ''),
                content=result.get('snippet', '')
            )

            scored_results.append({
                **result,
                'trust_score': score,
                'trust_level': level.value,
                'recommendation': self._get_recommendation(score)
            })

        # 信頼度でソート
        return sorted(scored_results, key=lambda x: x['trust_score'], reverse=True)

    def filter_by_trust_level(self,
                             results: List[Dict],
                             min_level: TrustLevel = TrustLevel.MEDIUM) -> List[Dict]:
        """信頼度レベルでフィルタリング"""
        level_values = {
            TrustLevel.VERY_LOW: 0,
            TrustLevel.LOW: 1,
            TrustLevel.MEDIUM: 2,
            TrustLevel.HIGH: 3,
            TrustLevel.VERY_HIGH: 4
        }

        min_level_value = level_values[min_level]

        filtered = []
        for result in results:
            result_level = result.get('trust_level', 'medium')
            result_level_value = level_values.get(TrustLevel(result_level), 2)

            if result_level_value >= min_level_value:
                filtered.append(result)

        return filtered

    def get_trust_summary(self, results: List[Dict]) -> Dict:
        """信頼度サマリーを取得"""
        if not results:
            return {"error": "結果がありません"}

        scores = [r.get('trust_score', 0) for r in results]

        return {
            "total_results": len(results),
            "average_trust_score": round(sum(scores) / len(scores), 1),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "high_confidence_results": len([s for s in scores if s >= 80]),
            "medium_confidence_results": len([s for s in scores if 40 <= s < 80]),
            "low_confidence_results": len([s for s in scores if s < 40])
        }
