"""
基本分析ロジックモジュール
ユーザープロフィールと市場データを分析して副業機会を提案
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from .profiler import UserProfile, ExperienceLevel, TimeCommitment

__all__ = ['SideHustleOpportunity', 'SideHustleAnalyzer']


@dataclass
class SideHustleOpportunity:
    """副業機会"""
    id: str
    title: str
    description: str
    required_skills: List[str]
    estimated_monthly_income: int  # 円
    time_commitment_hours: int  # 週当たりの時間
    difficulty_level: str  # beginner, intermediate, advanced
    platforms: List[str]
    match_score: float  # 0-100


class SideHustleAnalyzer:
    """副業機会の分析"""

    # 事前定義された副業機会
    PREDEFINED_OPPORTUNITIES = [
        {
            "id": "writing-content",
            "title": "コンテンツライティング",
            "description": "ブログ記事、SEO記事、ニュースレターなどの作成",
            "required_skills": ["writing", "research", "communication"],
            "estimated_monthly_income": 50000,
            "time_commitment_hours": 20,
            "difficulty_level": "beginner",
            "platforms": ["upwork", "fiverr", "coconala"]
        },
        {
            "id": "web-design",
            "title": "ウェブデザイン",
            "description": "ウェブサイト、ランディングページ、UIデザインなど",
            "required_skills": ["design", "html", "css"],
            "estimated_monthly_income": 100000,
            "time_commitment_hours": 25,
            "difficulty_level": "intermediate",
            "platforms": ["upwork", "fiverr"]
        },
        {
            "id": "freelance-programming",
            "title": "フリーランスプログラミング",
            "description": "ウェブアプリ、スクリプト、ツール開発など",
            "required_skills": ["python", "javascript", "programming"],
            "estimated_monthly_income": 150000,
            "time_commitment_hours": 30,
            "difficulty_level": "intermediate",
            "platforms": ["upwork", "fiverr"]
        },
        {
            "id": "data-analysis",
            "title": "データ分析・BIコンサル",
            "description": "エクセル、データベース、ダッシュボード作成",
            "required_skills": ["data analysis", "excel", "python"],
            "estimated_monthly_income": 120000,
            "time_commitment_hours": 20,
            "difficulty_level": "intermediate",
            "platforms": ["upwork", "coconala"]
        },
        {
            "id": "video-editing",
            "title": "動画編集",
            "description": "YouTube動画、TikTok、プロモーション動画など",
            "required_skills": ["video", "editing", "creative"],
            "estimated_monthly_income": 80000,
            "time_commitment_hours": 25,
            "difficulty_level": "beginner",
            "platforms": ["fiverr", "upwork", "coconala"]
        },
        {
            "id": "translation",
            "title": "翻訳・多言語対応",
            "description": "英語、中国語、日本語などの翻訳",
            "required_skills": ["translation", "languages", "communication"],
            "estimated_monthly_income": 70000,
            "time_commitment_hours": 15,
            "difficulty_level": "intermediate",
            "platforms": ["upwork", "coconala", "crowdworks"]
        },
        {
            "id": "social-media-management",
            "title": "SNS運用・マーケティング",
            "description": "SNSアカウント運用、コンテンツ企画、広告管理",
            "required_skills": ["marketing", "social media", "communication"],
            "estimated_monthly_income": 60000,
            "time_commitment_hours": 20,
            "difficulty_level": "intermediate",
            "platforms": ["coconala", "crowdworks"]
        },
        {
            "id": "virtual-assistant",
            "title": "バーチャルアシスタント",
            "description": "事務作業、メール管理、スケジュール管理など",
            "required_skills": ["organization", "communication", "time-management"],
            "estimated_monthly_income": 50000,
            "time_commitment_hours": 20,
            "difficulty_level": "beginner",
            "platforms": ["upwork", "fiverr"]
        },
        {
            "id": "consulting",
            "title": "業界コンサルティング",
            "description": "業界知識を活かしたアドバイス、メンタリング",
            "required_skills": ["consulting", "expertise", "communication"],
            "estimated_monthly_income": 200000,
            "time_commitment_hours": 15,
            "difficulty_level": "advanced",
            "platforms": ["upwork", "coconala"]
        },
        {
            "id": "course-creation",
            "title": "オンラインコース制作・販売",
            "description": "Udemy, Teachable等でコース販売",
            "required_skills": ["teaching", "content creation", "expertise"],
            "estimated_monthly_income": 100000,
            "time_commitment_hours": 30,
            "difficulty_level": "advanced",
            "platforms": ["upwork"]
        }
    ]

    def __init__(self):
        self.opportunities = self.PREDEFINED_OPPORTUNITIES

    def calculate_match_score(self,
                             profile: UserProfile,
                             opportunity: Dict) -> float:
        """副業機会とプロフィールのマッチスコア を計算（0-100）"""
        score = 0.0
        max_score = 100.0

        # スキルマッチング (40点)
        skill_match_score = 0.0
        required_skills = opportunity.get('required_skills', [])
        profile_skills_lower = [s.lower() for s in profile.skills]

        if required_skills:
            matched_skills = sum(1 for req_skill in required_skills
                               if req_skill.lower() in profile_skills_lower)
            skill_match_score = (matched_skills / len(required_skills)) * 40

        score += skill_match_score

        # 経験レベルマッチング (20点)
        opp_difficulty = opportunity.get('difficulty_level', 'intermediate')
        exp_level = profile.experience_level

        difficulty_map = {
            'beginner': ExperienceLevel.BEGINNER,
            'intermediate': ExperienceLevel.INTERMEDIATE,
            'advanced': ExperienceLevel.ADVANCED,
        }

        opp_exp_level = difficulty_map.get(opp_difficulty, ExperienceLevel.INTERMEDIATE)

        if exp_level == opp_exp_level:
            score += 20  # 完全マッチ
        elif (exp_level == ExperienceLevel.ADVANCED and
              opp_exp_level != ExperienceLevel.ADVANCED):
            score += 20  # 上位レベルでも可能
        elif (exp_level == ExperienceLevel.INTERMEDIATE and
              opp_exp_level == ExperienceLevel.BEGINNER):
            score += 20  # 初心者でも可能

        # 時間的余裕マッチング (20点)
        time_commitment = opportunity.get('time_commitment_hours', 0)

        hours_map = {
            TimeCommitment.PART_TIME: 10,
            TimeCommitment.SEMI_FULL_TIME: 20,
            TimeCommitment.FULL_TIME: 40,
        }

        available_hours = hours_map.get(profile.time_commitment, 10)

        if time_commitment <= available_hours:
            score += 20
        else:
            score += max(0, 20 * (available_hours / time_commitment))

        # 月収マッチング (20点)
        opportunity_income = opportunity.get('estimated_monthly_income', 0)
        target_income = profile.target_monthly_income

        if opportunity_income >= target_income * 0.8:
            score += 20
        else:
            score += 20 * (opportunity_income / (target_income or 1))

        return min(score, 100.0)

    def find_opportunities(self,
                          profile: UserProfile,
                          top_n: int = 3) -> List[SideHustleOpportunity]:
        """プロフィールに最適な副業機会を検出"""

        scored_opportunities = []

        for opp in self.opportunities:
            match_score = self.calculate_match_score(profile, opp)
            scored_opportunities.append((opp, match_score))

        # スコアでソート（降順）
        scored_opportunities.sort(key=lambda x: x[1], reverse=True)

        # 上位 N 個を返す
        result = []
        for opp, score in scored_opportunities[:top_n]:
            opportunity = SideHustleOpportunity(
                id=opp['id'],
                title=opp['title'],
                description=opp['description'],
                required_skills=opp['required_skills'],
                estimated_monthly_income=opp['estimated_monthly_income'],
                time_commitment_hours=opp['time_commitment_hours'],
                difficulty_level=opp['difficulty_level'],
                platforms=opp['platforms'],
                match_score=round(score, 1)
            )
            result.append(opportunity)

        return result

    def get_roadmap(self, profile: UserProfile) -> Dict:
        """ユーザー向けのロードマップを作成"""

        opportunities = self.find_opportunities(profile, top_n=1)

        if not opportunities:
            return {"error": "マッチする副業が見つかりませんでした"}

        top_opportunity = opportunities[0]

        roadmap = {
            "opportunity": {
                "title": top_opportunity.title,
                "description": top_opportunity.description,
                "match_score": top_opportunity.match_score
            },
            "phases": {
                "initial": {
                    "duration_weeks": 2,
                    "tasks": [
                        "ポートフォリオの作成",
                        "プロフィールの最適化",
                        "初案件の獲得戦略"
                    ]
                },
                "growth": {
                    "duration_weeks": 4,
                    "tasks": [
                        "単価交渉",
                        "評価・レビューの構築",
                        "リピート客の確保"
                    ]
                },
                "stable": {
                    "duration_weeks": 4,
                    "tasks": [
                        "定期案件の確保",
                        "スキル拡張",
                        "新規市場への展開"
                    ]
                }
            },
            "income_projection": {
                "week_2": int(top_opportunity.estimated_monthly_income * 0.2),
                "week_4": int(top_opportunity.estimated_monthly_income * 0.5),
                "month_3": int(top_opportunity.estimated_monthly_income * 0.8),
            }
        }

        return roadmap

    def get_skill_gap_analysis(self, profile: UserProfile) -> Dict:
        """スキルギャップ分析"""

        opportunities = self.find_opportunities(profile, top_n=1)

        if not opportunities:
            return {"error": "分析対象がありません"}

        top_opportunity = opportunities[0]
        profile_skills_lower = [s.lower() for s in profile.skills]
        required_skills = [s.lower() for s in top_opportunity.required_skills]

        gap_skills = [s for s in required_skills if s not in profile_skills_lower]

        return {
            "opportunity": top_opportunity.title,
            "current_skills": profile.skills,
            "required_skills": top_opportunity.required_skills,
            "gap_skills": gap_skills,
            "gap_count": len(gap_skills),
            "readiness_percentage": round(
                ((len(required_skills) - len(gap_skills)) / len(required_skills) * 100)
                if required_skills else 0, 1
            ),
            "learning_recommendations": [
                f"「{skill}」スキルの習得" for skill in gap_skills[:3]
            ]
        }
