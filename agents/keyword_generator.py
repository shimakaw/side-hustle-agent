"""
キーワード自動生成モジュール
ユーザープロフィールから検索キーワードを生成
"""

from typing import List, Dict, Set
from .profiler import UserProfile, ExperienceLevel, TimeCommitment


class KeywordGenerator:
    """検索キーワード生成"""

    # スキル別のキーワードマッピング
    SKILL_KEYWORDS = {
        "python": ["python developer", "python freelance", "automation", "データ分析"],
        "javascript": ["javascript developer", "web development", "frontend", "ウェブ制作"],
        "design": ["graphic design", "UI/UX design", "logo design", "デザイン"],
        "writing": ["content writing", "copywriting", "ライティング", "記事執筆"],
        "marketing": ["digital marketing", "social media", "SEO", "マーケティング"],
        "data analysis": ["data analyst", "excel", "spreadsheet", "データ分析"],
        "translation": ["translation", "翻訳", "通訳", "言語"],
        "video": ["video editing", "youtube", "animation", "動画編集"],
        "music": ["music production", "audio", "podcast", "音楽"],
        "consulting": ["consulting", "business", "strategy", "コンサルティング"],
    }

    # 経験レベル別のキーワード
    EXPERIENCE_KEYWORDS = {
        ExperienceLevel.BEGINNER: ["entry level", "ビギナー向け", "初心者", "学習"],
        ExperienceLevel.INTERMEDIATE: ["mid-level", "中級", "経験者", "スキルアップ"],
        ExperienceLevel.ADVANCED: ["senior", "expert", "プロ", "マスター"],
    }

    # 時間的余裕別のキーワード
    COMMITMENT_KEYWORDS = {
        TimeCommitment.PART_TIME: ["part-time", "兼業", "副業", "時間短縮"],
        TimeCommitment.SEMI_FULL_TIME: ["flexible hours", "リモート", "自由な時間"],
        TimeCommitment.FULL_TIME: ["full-time", "専属", "継続案件"],
    }

    # 月収別のキーワード
    INCOME_KEYWORDS = {
        "budget_10k": ["小額", "お試し", "初心者向け"],
        "budget_30k": ["月3万円", "副業", "小遣い稼ぎ"],
        "budget_50k": ["月5万円", "本格副業"],
        "budget_100k": ["月10万円", "本業並み"],
        "budget_300k": ["月30万円", "専業"],
    }

    def __init__(self):
        pass

    def get_income_bucket(self, monthly_income: int) -> str:
        """月収をバケット分類"""
        if monthly_income < 30000:
            return "budget_10k"
        elif monthly_income < 50000:
            return "budget_30k"
        elif monthly_income < 100000:
            return "budget_50k"
        elif monthly_income < 300000:
            return "budget_100k"
        else:
            return "budget_300k"

    def generate_keywords(self, profile: UserProfile, count: int = 6) -> List[str]:
        """プロフィールからキーワードを生成"""
        keywords: Set[str] = set()

        # スキルベースのキーワード
        for skill in profile.skills[:3]:  # 最初の3つのスキル
            skill_lower = skill.lower()
            if skill_lower in self.SKILL_KEYWORDS:
                keywords.update(self.SKILL_KEYWORDS[skill_lower][:2])
            else:
                # スキルそのものをキーワードに
                keywords.add(skill)
                keywords.add(f"{skill} freelance")

        # 経験レベルのキーワード
        if profile.experience_level in self.EXPERIENCE_KEYWORDS:
            keywords.update(self.EXPERIENCE_KEYWORDS[profile.experience_level][:1])

        # 時間的余裕のキーワード
        if profile.time_commitment in self.COMMITMENT_KEYWORDS:
            keywords.update(self.COMMITMENT_KEYWORDS[profile.time_commitment][:1])

        # 月収のキーワード
        income_bucket = self.get_income_bucket(profile.target_monthly_income)
        if income_bucket in self.INCOME_KEYWORDS:
            keywords.update(self.INCOME_KEYWORDS[income_bucket][:1])

        # プラットフォーム別のキーワード
        if profile.preferred_platforms:
            platform = profile.preferred_platforms[0]
            keywords.add(f"{platform} jobs")
            keywords.add(platform)

        # リスト化して、指定数分返す
        keyword_list = sorted(list(keywords))[:count]

        # キーワードが不足しているなら、汎用キーワードを追加
        if len(keyword_list) < count:
            generic_keywords = [
                "remote work",
                "freelance",
                "side hustle",
                "work from home",
                "online job"
            ]
            for keyword in generic_keywords:
                if keyword not in keyword_list and len(keyword_list) < count:
                    keyword_list.append(keyword)

        return keyword_list[:count]

    def generate_platform_specific_keywords(self,
                                           profile: UserProfile,
                                           platform: str) -> List[str]:
        """プラットフォーム固有のキーワードを生成"""
        platform_lower = platform.lower()

        base_keywords = self.generate_keywords(profile, 3)

        platform_specific = {
            "upwork": ["upwork", "oDesk", "elance"],
            "fiverr": ["fiverr", "gig", "short-term"],
            "coconala": ["coconala", "ココナラ", "日本"],
            "crowdworks": ["crowdworks", "クラウドワークス", "日本"],
            "lancers": ["lancers", "ランサーズ", "日本"],
        }

        keywords = list(base_keywords)
        if platform_lower in platform_specific:
            keywords.extend(platform_specific[platform_lower][:2])

        return keywords[:6]

    def generate_analysis_keywords(self, profile: UserProfile) -> Dict[str, List[str]]:
        """市場分析用の複数キーワードセットを生成"""
        return {
            "general": self.generate_keywords(profile, 5),
            "upwork": self.generate_platform_specific_keywords(profile, "upwork"),
            "fiverr": self.generate_platform_specific_keywords(profile, "fiverr"),
            "local": self.generate_platform_specific_keywords(profile, "coconala"),
            "market": [
                f"{profile.skills[0] if profile.skills else 'freelance'} market",
                "freelance rates",
                "market trends",
                "compensation",
                "average salary"
            ]
        }

    def validate_keywords(self, keywords: List[str]) -> bool:
        """キーワードのバリデーション"""
        if not keywords or len(keywords) == 0:
            return False

        for keyword in keywords:
            if not isinstance(keyword, str) or len(keyword.strip()) == 0:
                return False
            if len(keyword) > 100:
                return False

        return True

    def merge_keywords(self, *keyword_lists) -> List[str]:
        """複数のキーワードリストをマージ（重複排除）"""
        merged = set()
        for keywords in keyword_lists:
            if isinstance(keywords, list):
                merged.update(keywords)

        return sorted(list(merged))
