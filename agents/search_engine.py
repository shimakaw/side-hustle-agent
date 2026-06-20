"""
Web検索エンジンモジュール
キーワードから市場情報を検索
"""

from typing import List, Dict, Optional, Tuple
import json
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SearchResult:
    """検索結果"""
    title: str
    url: str
    snippet: str
    source: str
    relevance_score: float = 0.5


class SearchEngine:
    """Web検索エンジン"""

    MOCK_RESULTS = {
        "python freelance": [
            {
                "title": "Python Developer Freelance Opportunities",
                "url": "https://upwork.com/jobs/search/?q=python",
                "snippet": "High demand for Python developers. Average rate: $50-150/hour",
                "source": "upwork"
            },
            {
                "title": "Python Programming Jobs on Fiverr",
                "url": "https://fiverr.com/search/gigs?q=python",
                "snippet": "1000+ active Python gigs. Entry level starts at $5-20",
                "source": "fiverr"
            }
        ],
        "freelance rates": [
            {
                "title": "2024 Freelance Rate Guide",
                "url": "https://blog.upwork.com/rates",
                "snippet": "Average freelance rates by skill. Updated for 2024",
                "source": "upwork"
            }
        ],
        "data analyst freelance": [
            {
                "title": "Data Analysis Jobs",
                "url": "https://upwork.com/jobs/search/?q=data+analysis",
                "snippet": "Data analysts earn $60-200/hour on average",
                "source": "upwork"
            }
        ],
        "web design jobs": [
            {
                "title": "Web Design Freelance Work",
                "url": "https://upwork.com/jobs/search/?q=web+design",
                "snippet": "Web designers average $40-120/hour",
                "source": "upwork"
            }
        ]
    }

    def __init__(self, enable_mock: bool = True):
        """
        Args:
            enable_mock: True なら模擬データを使用（テスト用）
        """
        self.enable_mock = enable_mock
        self.search_history: List[Dict] = []

    def search(self,
              keywords: List[str],
              max_results: int = 10) -> Tuple[bool, List[SearchResult]]:
        """キーワードで検索"""

        if not keywords:
            return False, []

        results = []
        query = " ".join(keywords[:3])  # 最初の3つのキーワードで検索

        try:
            if self.enable_mock:
                results = self._search_mock(query, max_results)
            else:
                results = self._search_real(query, max_results)

            # 検索履歴に記録
            self.search_history.append({
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "result_count": len(results)
            })

            return True, results

        except Exception as e:
            print(f"検索エラー: {e}")
            return False, []

    def _search_mock(self, query: str, max_results: int) -> List[SearchResult]:
        """模擬検索（テスト用）"""

        # キーワードに部分マッチするモック結果を返す
        query_lower = query.lower()

        matching_results = []
        for mock_query, mock_data in self.MOCK_RESULTS.items():
            if any(word in query_lower for word in mock_query.split()):
                matching_results.extend(mock_data)

        # マッチなしの場合は汎用結果を返す
        if not matching_results:
            matching_results = [
                {
                    "title": f"Results for {query}",
                    "url": f"https://example.com/search?q={query}",
                    "snippet": f"Search results for freelance opportunities in {query}",
                    "source": "example"
                }
            ]

        # SearchResult オブジェクトに変換
        results = []
        for i, data in enumerate(matching_results[:max_results]):
            result = SearchResult(
                title=data['title'],
                url=data['url'],
                snippet=data['snippet'],
                source=data['source'],
                relevance_score=round(1.0 - (i * 0.05), 2)  # 順序で減少
            )
            results.append(result)

        return results

    def _search_real(self, query: str, max_results: int) -> List[SearchResult]:
        """実際のWeb検索（実装時）"""
        # TODO: 実装時に Google Custom Search API や他のAPI統合
        # 現在はモック結果を返す
        return self._search_mock(query, max_results)

    def parallel_search(self, keyword_sets: Dict[str, List[str]]) -> Dict[str, List[SearchResult]]:
        """複数のキーワードセットで並列検索"""

        results = {}
        for key, keywords in keyword_sets.items():
            success, search_results = self.search(keywords, max_results=5)
            results[key] = search_results if success else []

        return results

    def get_search_history(self) -> List[Dict]:
        """検索履歴を取得"""
        return self.search_history

    def filter_by_source(self,
                        results: List[SearchResult],
                        source: str) -> List[SearchResult]:
        """ソースでフィルタリング"""
        return [r for r in results if r.source == source]

    def filter_by_relevance(self,
                           results: List[SearchResult],
                           min_score: float = 0.5) -> List[SearchResult]:
        """関連度でフィルタリング"""
        return [r for r in results if r.relevance_score >= min_score]

    def to_dict(self, result: SearchResult) -> Dict:
        """SearchResult を辞書に変換"""
        return asdict(result)

    def to_json(self, result: SearchResult) -> str:
        """SearchResult を JSON に変換"""
        return json.dumps(self.to_dict(result), ensure_ascii=False, indent=2)
