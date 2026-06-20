"""
キャッシュ管理モジュール
検索結果やプラットフォームデータをキャッシュ
"""

from typing import Optional, Dict, Any
import json
import os
from datetime import datetime, timedelta


class CacheEntry:
    """キャッシュエントリ"""

    def __init__(self, key: str, value: Any, ttl_hours: int = 24):
        self.key = key
        self.value = value
        self.created_at = datetime.now()
        self.ttl = timedelta(hours=ttl_hours)

    def is_expired(self) -> bool:
        """キャッシュが有効期限切れかどうか"""
        return datetime.now() > (self.created_at + self.ttl)

    def get_age_minutes(self) -> int:
        """キャッシュの経過時間（分）"""
        age = datetime.now() - self.created_at
        return int(age.total_seconds() / 60)

    def to_dict(self) -> Dict:
        """辞書に変換"""
        return {
            "key": self.key,
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "age_minutes": self.get_age_minutes(),
            "is_expired": self.is_expired()
        }


class CacheManager:
    """キャッシュ管理"""

    def __init__(self, cache_dir: str = "data/cache", default_ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.default_ttl_hours = default_ttl_hours
        self.memory_cache: Dict[str, CacheEntry] = {}

        # ディレクトリを作成
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)

    def set(self, key: str, value: Any, ttl_hours: Optional[int] = None) -> bool:
        """キャッシュに設定"""
        try:
            ttl = ttl_hours or self.default_ttl_hours
            entry = CacheEntry(key, value, ttl)

            # メモリキャッシュに保存
            self.memory_cache[key] = entry

            # ファイルにも保存
            self._save_to_file(key, entry)

            return True

        except Exception as e:
            print(f"キャッシュ設定エラー: {e}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """キャッシュから取得"""
        try:
            # メモリキャッシュをチェック
            if key in self.memory_cache:
                entry = self.memory_cache[key]
                if not entry.is_expired():
                    return entry.value
                else:
                    # 期限切れなので削除
                    del self.memory_cache[key]

            # ファイルから読み込み
            entry = self._load_from_file(key)
            if entry and not entry.is_expired():
                self.memory_cache[key] = entry
                return entry.value

            return None

        except Exception as e:
            print(f"キャッシュ取得エラー: {e}")
            return None

    def exists(self, key: str) -> bool:
        """キャッシュが存在し、有効期限内かチェック"""
        return self.get(key) is not None

    def delete(self, key: str) -> bool:
        """キャッシュを削除"""
        try:
            if key in self.memory_cache:
                del self.memory_cache[key]

            cache_file = self._get_cache_filepath(key)
            if os.path.exists(cache_file):
                os.remove(cache_file)

            return True

        except Exception as e:
            print(f"キャッシュ削除エラー: {e}")
            return False

    def clear(self) -> bool:
        """すべてのキャッシュをクリア"""
        try:
            self.memory_cache.clear()

            # ファイルをクリア
            if os.path.exists(self.cache_dir):
                for filename in os.listdir(self.cache_dir):
                    filepath = os.path.join(self.cache_dir, filename)
                    if os.path.isfile(filepath):
                        os.remove(filepath)

            return True

        except Exception as e:
            print(f"キャッシュクリアエラー: {e}")
            return False

    def get_stats(self) -> Dict:
        """キャッシュ統計を取得"""
        valid_count = 0
        expired_count = 0
        total_size = 0

        for entry in self.memory_cache.values():
            if entry.is_expired():
                expired_count += 1
            else:
                valid_count += 1

        # ファイルサイズを計算
        if os.path.exists(self.cache_dir):
            for filename in os.listdir(self.cache_dir):
                filepath = os.path.join(self.cache_dir, filename)
                if os.path.isfile(filepath):
                    total_size += os.path.getsize(filepath)

        return {
            "valid_entries": valid_count,
            "expired_entries": expired_count,
            "total_entries": len(self.memory_cache),
            "total_size_bytes": total_size,
            "cache_dir": self.cache_dir
        }

    def clean_expired(self) -> int:
        """期限切れエントリを削除"""
        expired_keys = [
            key for key, entry in self.memory_cache.items()
            if entry.is_expired()
        ]

        for key in expired_keys:
            self.delete(key)

        return len(expired_keys)

    def _get_cache_filepath(self, key: str) -> str:
        """キャッシュファイルパスを取得"""
        # キーをファイル名に変換（安全にする）
        safe_key = key.replace("/", "_").replace("\\", "_")
        return os.path.join(self.cache_dir, f"{safe_key}.json")

    def _save_to_file(self, key: str, entry: CacheEntry) -> bool:
        """ファイルに保存"""
        try:
            filepath = self._get_cache_filepath(key)

            data = {
                "key": entry.key,
                "value": entry.value,
                "created_at": entry.created_at.isoformat(),
                "ttl_hours": entry.ttl.total_seconds() / 3600
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"ファイル保存エラー: {e}")
            return False

    def _load_from_file(self, key: str) -> Optional[CacheEntry]:
        """ファイルから読み込み"""
        try:
            filepath = self._get_cache_filepath(key)

            if not os.path.exists(filepath):
                return None

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            created_at = datetime.fromisoformat(data['created_at'])
            ttl_hours = data.get('ttl_hours', self.default_ttl_hours)

            entry = CacheEntry(data['key'], data['value'], int(ttl_hours))
            entry.created_at = created_at

            return entry

        except Exception as e:
            print(f"ファイル読み込みエラー: {e}")
            return None

    def get_all_keys(self) -> list:
        """すべてのキャッシュキーを取得"""
        return list(self.memory_cache.keys())

    def get_entry_info(self, key: str) -> Optional[Dict]:
        """エントリ情報を取得"""
        if key not in self.memory_cache:
            return None

        entry = self.memory_cache[key]
        return entry.to_dict()
