"""
プロファイラーのユニットテスト
"""

import unittest
import sys
import os

# パスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from agents.profiler import UserProfile, UserProfiler, ExperienceLevel, TimeCommitment


class TestUserProfile(unittest.TestCase):
    """UserProfile クラスのテスト"""

    def test_profile_creation(self):
        """プロフィール作成テスト"""
        profile = UserProfile(
            name="田中太郎",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["python", "data analysis"],
            target_monthly_income=50000,
            time_commitment=TimeCommitment.PART_TIME
        )

        self.assertEqual(profile.name, "田中太郎")
        self.assertEqual(profile.experience_level, ExperienceLevel.BEGINNER)
        self.assertEqual(len(profile.skills), 2)
        self.assertEqual(profile.target_monthly_income, 50000)

    def test_profile_to_dict(self):
        """プロフィールの辞書変換テスト"""
        profile = UserProfile(
            name="山田次郎",
            experience_level=ExperienceLevel.INTERMEDIATE,
            skills=["javascript"],
            target_monthly_income=100000,
            time_commitment=TimeCommitment.SEMI_FULL_TIME
        )

        profile_dict = profile.to_dict()

        self.assertEqual(profile_dict['name'], "山田次郎")
        self.assertEqual(profile_dict['experience_level'], "intermediate")
        self.assertIn("javascript", profile_dict['skills'])


class TestUserProfiler(unittest.TestCase):
    """UserProfiler クラスのテスト"""

    def setUp(self):
        self.profiler = UserProfiler()

    def test_validate_profile_valid(self):
        """バリデーション：有効なプロフィール"""
        profile = UserProfile(
            name="有効なユーザー",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["python"],
            target_monthly_income=50000,
            time_commitment=TimeCommitment.PART_TIME
        )

        is_valid, errors = self.profiler.validate_profile(profile)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_validate_profile_invalid_name(self):
        """バリデーション：無効な名前"""
        profile = UserProfile(
            name="",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["python"],
            target_monthly_income=50000,
            time_commitment=TimeCommitment.PART_TIME
        )

        is_valid, errors = self.profiler.validate_profile(profile)
        self.assertFalse(is_valid)
        self.assertTrue(any("名前" in error for error in errors))

    def test_validate_profile_invalid_income(self):
        """バリデーション：無効な月収"""
        profile = UserProfile(
            name="テストユーザー",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["python"],
            target_monthly_income=1000,  # 最小値より低い
            time_commitment=TimeCommitment.PART_TIME
        )

        is_valid, errors = self.profiler.validate_profile(profile)
        self.assertFalse(is_valid)
        self.assertTrue(any("月収" in error for error in errors))

    def test_create_profile(self):
        """プロフィール作成テスト"""
        success, result = self.profiler.create_profile(
            name="新規ユーザー",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["writing", "research"],
            target_monthly_income=50000,
            time_commitment=TimeCommitment.PART_TIME
        )

        self.assertTrue(success)
        self.assertIsInstance(result, UserProfile)
        self.assertEqual(result.name, "新規ユーザー")

    def test_create_profile_invalid_data(self):
        """無効なデータでのプロフィール作成"""
        success, result = self.profiler.create_profile(
            name="",
            experience_level=ExperienceLevel.BEGINNER,
            skills=[],
            target_monthly_income=5000,  # 最小値より低い
            time_commitment=TimeCommitment.PART_TIME
        )

        self.assertFalse(success)
        self.assertIsInstance(result, str)

    def test_get_profile(self):
        """プロフィール取得テスト"""
        self.profiler.create_profile(
            name="検索対象",
            experience_level=ExperienceLevel.INTERMEDIATE,
            skills=["python"],
            target_monthly_income=100000,
            time_commitment=TimeCommitment.SEMI_FULL_TIME
        )

        profile = self.profiler.get_profile("検索対象")
        self.assertIsNotNone(profile)
        self.assertEqual(profile.name, "検索対象")

    def test_list_profiles(self):
        """プロフィール一覧取得テスト"""
        self.profiler.create_profile(
            name="ユーザー1",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["python"],
            target_monthly_income=50000,
            time_commitment=TimeCommitment.PART_TIME
        )
        self.profiler.create_profile(
            name="ユーザー2",
            experience_level=ExperienceLevel.INTERMEDIATE,
            skills=["javascript"],
            target_monthly_income=100000,
            time_commitment=TimeCommitment.SEMI_FULL_TIME
        )

        profiles = self.profiler.list_profiles()
        self.assertEqual(len(profiles), 2)

    def test_delete_profile(self):
        """プロフィール削除テスト"""
        self.profiler.create_profile(
            name="削除対象",
            experience_level=ExperienceLevel.BEGINNER,
            skills=["python"],
            target_monthly_income=50000,
            time_commitment=TimeCommitment.PART_TIME
        )

        deleted = self.profiler.delete_profile("削除対象")
        self.assertTrue(deleted)

        profile = self.profiler.get_profile("削除対象")
        self.assertIsNone(profile)


if __name__ == '__main__':
    unittest.main()
