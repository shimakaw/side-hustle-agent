"""
ローカルファイル参照モジュール
MANIFEST.json や研究資料からデータを抽出
"""

import json
import os
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


class FileHandler:
    """ローカルファイル参照"""

    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.manifest_cache: Optional[Dict] = None
        self.research_cache: Optional[str] = None

    def resolve_path(self, filepath: str) -> str:
        """相対パスを絶対パスに解決"""
        if os.path.isabs(filepath):
            return filepath
        return os.path.join(self.base_path, filepath)

    def load_manifest(self, manifest_path: str = "../../../products/MANIFEST.json") -> Optional[Dict]:
        """MANIFEST.json を読み込む"""
        try:
            resolved_path = self.resolve_path(manifest_path)

            if not os.path.exists(resolved_path):
                print(f"警告: MANIFEST.json が見つかりません: {resolved_path}")
                return None

            with open(resolved_path, 'r', encoding='utf-8') as f:
                self.manifest_cache = json.load(f)
                return self.manifest_cache

        except json.JSONDecodeError as e:
            print(f"JSON解析エラー: {e}")
            return None
        except Exception as e:
            print(f"ファイル読み込みエラー: {e}")
            return None

    def get_all_products(self) -> List[Dict]:
        """全成果物を取得"""
        if self.manifest_cache is None:
            self.load_manifest()

        if self.manifest_cache is None:
            return []

        return self.manifest_cache.get('products', [])

    def get_products_by_category(self, category: str) -> List[Dict]:
        """カテゴリ別に成果物を取得"""
        products = self.get_all_products()
        return [p for p in products if p.get('category') == category]

    def get_products_by_tags(self, tags: List[str]) -> List[Dict]:
        """タグで成果物を検索"""
        products = self.get_all_products()
        results = []
        for product in products:
            product_tags = product.get('tags', [])
            if any(tag in product_tags for tag in tags):
                results.append(product)
        return results

    def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """ID で成果物を取得"""
        products = self.get_all_products()
        for product in products:
            if product.get('id') == product_id:
                return product
        return None

    def get_categories(self) -> List[str]:
        """全カテゴリ一覧を取得"""
        if self.manifest_cache is None:
            self.load_manifest()

        if self.manifest_cache is None:
            return []

        return self.manifest_cache.get('categories', [])

    def load_research_file(self, filepath: str) -> Optional[str]:
        """研究資料ファイルを読み込む（markdown）"""
        try:
            resolved_path = self.resolve_path(filepath)

            if not os.path.exists(resolved_path):
                print(f"警告: ファイルが見つかりません: {resolved_path}")
                return None

            with open(resolved_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content

        except Exception as e:
            print(f"ファイル読み込みエラー: {e}")
            return None

    def extract_keywords_from_file(self, filepath: str) -> List[str]:
        """ファイルからキーワードを抽出"""
        content = self.load_research_file(filepath)
        if not content:
            return []

        # 簡易的なキーワード抽出（markdown の見出しから）
        lines = content.split('\n')
        keywords = []

        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                # 見出しから # を除去
                keyword = line.lstrip('#').strip()
                if keyword and len(keyword) > 2:
                    keywords.append(keyword)

        return keywords[:10]  # 最大10個

    def get_ai_fukugyo_data(self) -> Dict:
        """AI副業プロジェクトのデータを取得"""
        data = {
            "research": None,
            "manuscript": None
        }

        # research.md を読み込む
        research_path = "../../../products/003_ai_fukugyo/research.md"
        data["research"] = self.load_research_file(research_path)

        # manuscript.md を読み込む
        manuscript_path = "../../../products/003_ai_fukugyo/manuscript.md"
        data["manuscript"] = self.load_research_file(manuscript_path)

        return data

    def list_files(self, directory: str) -> List[str]:
        """ディレクトリ内のファイル一覧"""
        try:
            resolved_path = self.resolve_path(directory)
            if not os.path.exists(resolved_path):
                return []

            files = []
            for item in os.listdir(resolved_path):
                full_path = os.path.join(resolved_path, item)
                if os.path.isfile(full_path):
                    files.append(item)
            return sorted(files)

        except Exception as e:
            print(f"ディレクトリ読み込みエラー: {e}")
            return []

    def file_exists(self, filepath: str) -> bool:
        """ファイルが存在するか確認"""
        resolved_path = self.resolve_path(filepath)
        return os.path.exists(resolved_path)

    def get_file_info(self, filepath: str) -> Optional[Dict]:
        """ファイル情報を取得"""
        try:
            resolved_path = self.resolve_path(filepath)
            if not os.path.exists(resolved_path):
                return None

            stat_info = os.stat(resolved_path)
            return {
                "path": filepath,
                "size_bytes": stat_info.st_size,
                "modified": stat_info.st_mtime,
                "is_file": os.path.isfile(resolved_path)
            }

        except Exception as e:
            print(f"ファイル情報取得エラー: {e}")
            return None

    def search_in_files(self, directory: str, keyword: str) -> List[str]:
        """ディレクトリ内のファイルからキーワードを検索"""
        results = []
        resolved_dir = self.resolve_path(directory)

        if not os.path.exists(resolved_dir):
            return results

        for filename in os.listdir(resolved_dir):
            filepath = os.path.join(resolved_dir, filename)
            if os.path.isfile(filepath) and filename.endswith('.md'):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if keyword.lower() in content.lower():
                            results.append(filename)
                except Exception:
                    pass

        return results
