"""
ユーザープロファイリングモジュール
ユーザーの情報を収集・検証・保存
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Union, Tuple
from enum import Enum
import json
from datetime import datetime


class ExperienceLevel(Enum):
    """副業経験レベル"""
    BEGINNER = "beginner"  # 未経験
    INTERMEDIATE = "intermediate"  # 1-3ヶ月経験
    ADVANCED = "advanced"  # 3ヶ月以上


class TimeCommitment(Enum):
    """時間的な余裕"""
    PART_TIME = "part_time"  # 週5-10時間
    SEMI_FULL_TIME = "semi_full_time"  # 週10-20時間
    FULL_TIME = "full_time"  # 週20時間以上


@dataclass
class UserProfile:
    """ユーザープロフィール"""
    name: str
    experience_level: ExperienceLevel
    skills: List[str]
    target_monthly_income: int  # 円
    time_commitment: TimeCommitment
    current_occupation: Optional[str] = None
    preferred_platforms: List[str] = None
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.preferred_platforms is None:
            self.preferred_platforms = []

    def to_dict(self) -> Dict:
        """辞書に変換"""
        return {
            "name": self.name,
            "experience_level": self.experience_level.value,
            "skills": self.skills,
            "target_monthly_income": self.target_monthly_income,
            "time_commitment": self.time_commitment.value,
            "current_occupation": self.current_occupation,
            "preferred_platforms": self.preferred_platforms,
            "created_at": self.created_at
        }

    def to_json(self) -> str:
        """JSON文字列に変換"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class UserProfiler:
    """ユーザープロファイリング"""

    VALID_PLATFORMS = ["upwork", "fiverr", "coconala", "crowdworks", "lancers"]
    MIN_SKILLS = 1
    MAX_SKILLS = 10
    MIN_INCOME = 10000  # 最低月10,000円
    MAX_INCOME = 10000000  # 最高月1000万円

    def __init__(self):
        self.profiles: Dict[str, UserProfile] = {}

    def validate_profile(self, profile: UserProfile) -> Tuple[bool, List[str]]:
        """プロフィールのバリデーション"""
        errors = []

        # 名前のバリデーション
        if not profile.name or len(profile.name.strip()) == 0:
            errors.append("名前は必須です")
        elif len(profile.name) > 50:
            errors.append("名前は50文字以内です")

        # スキルのバリデーション
        if not profile.skills:
            errors.append("スキルは1つ以上必要です")
        elif len(profile.skills) > self.MAX_SKILLS:
            errors.append(f"スキルは{self.MAX_SKILLS}個以下にしてください")
        else:
            for skill in profile.skills:
                if not isinstance(skill, str) or len(skill.strip()) == 0:
                    errors.append("スキルは空でない文字列である必要があります")
                    break
                if len(skill) > 30:
                    errors.append("各スキルは30文字以内です")
                    break

        # 月収のバリデーション
        if profile.target_monthly_income < self.MIN_INCOME:
            errors.append(f"目標月収は{self.MIN_INCOME:,}円以上です")
        elif profile.target_monthly_income > self.MAX_INCOME:
            errors.append(f"目標月収は{self.MAX_INCOME:,}円以下です")

        # プラットフォームのバリデーション
        for platform in profile.preferred_platforms:
            if platform not in self.VALID_PLATFORMS:
                errors.append(f"無効なプラットフォーム: {platform}")

        return len(errors) == 0, errors

    def create_profile(self,
                      name: str,
                      experience_level: ExperienceLevel,
                      skills: List[str],
                      target_monthly_income: int,
                      time_commitment: TimeCommitment,
                      current_occupation: Optional[str] = None,
                      preferred_platforms: List[str] = None) -> Tuple[bool, Union[UserProfile, str]]:
        """プロフィール作成"""

        if preferred_platforms is None:
            preferred_platforms = []

        profile = UserProfile(
            name=name,
            experience_level=experience_level,
            skills=skills,
            target_monthly_income=target_monthly_income,
            time_commitment=time_commitment,
            current_occupation=current_occupation,
            preferred_platforms=preferred_platforms
        )

        # バリデーション
        is_valid, errors = self.validate_profile(profile)
        if not is_valid:
            return False, f"バリデーションエラー:\n" + "\n".join(errors)

        # 保存
        self.profiles[name] = profile
        return True, profile

    def get_profile(self, name: str) -> Optional[UserProfile]:
        """プロフィール取得"""
        return self.profiles.get(name)

    def list_profiles(self) -> List[UserProfile]:
        """全プロフィール一覧"""
        return list(self.profiles.values())

    def update_profile(self, name: str, **kwargs) -> tuple[bool, str]:
        """プロフィール更新"""
        if name not in self.profiles:
            return False, f"プロフィール '{name}' が見つかりません"

        profile = self.profiles[name]

        # 更新可能なフィールド
        updatable_fields = {
            "skills": list,
            "target_monthly_income": int,
            "time_commitment": TimeCommitment,
            "preferred_platforms": list,
            "current_occupation": str
        }

        for key, value in kwargs.items():
            if key not in updatable_fields:
                return False, f"フィールド '{key}' は更新できません"

            if value is not None:
                setattr(profile, key, value)

        # 更新後のバリデーション
        is_valid, errors = self.validate_profile(profile)
        if not is_valid:
            return False, f"バリデーションエラー:\n" + "\n".join(errors)

        return True, "プロフィールを更新しました"

    def delete_profile(self, name: str) -> bool:
        """プロフィール削除"""
        if name in self.profiles:
            del self.profiles[name]
            return True
        return False

    def save_to_file(self, filepath: str) -> bool:
        """プロフィールをファイルに保存"""
        try:
            data = {name: profile.to_dict() for name, profile in self.profiles.items()}
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"ファイル保存エラー: {e}")
            return False

    def load_from_file(self, filepath: str) -> bool:
        """ファイルからプロフィールを読み込む"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for name, profile_data in data.items():
                profile = UserProfile(
                    name=profile_data['name'],
                    experience_level=ExperienceLevel(profile_data['experience_level']),
                    skills=profile_data['skills'],
                    target_monthly_income=profile_data['target_monthly_income'],
                    time_commitment=TimeCommitment(profile_data['time_commitment']),
                    current_occupation=profile_data.get('current_occupation'),
                    preferred_platforms=profile_data.get('preferred_platforms', []),
                    created_at=profile_data.get('created_at')
                )
                self.profiles[name] = profile
            return True
        except Exception as e:
            print(f"ファイル読み込みエラー: {e}")
            return False
