"""
テンプレート生成モジュール
Claude API を使用してテンプレートを生成
"""

from typing import Optional, Dict, List
from dataclasses import dataclass
from .profiler import UserProfile, ExperienceLevel


@dataclass
class GeneratedTemplate:
    """生成されたテンプレート"""
    template_type: str
    content: str
    platform: str
    is_editable: bool = True


class TemplateGenerator:
    """テンプレート生成"""

    # Claude API のモック返答（テスト用）
    MOCK_TEMPLATES = {
        "portfolio_upwork": """
# プロフィール

こんにちは！{name}です。

## 自己紹介
私は{experience_level}のフリーランス専門家で、{skills_str}に特化しています。

## スキル
{skills_list}

## 実績
- {skill_1}での実績が豊富
- クライアント満足度: 90%以上
- 納期遵守率: 100%

## レート
目標月収: ¥{target_income:,}

ご質問やお仕事の依頼があれば、いつでもお気軽にお問い合わせください！
        """,

        "sales_email": """
件名: {skill_1}でお力になります！

{name}と申します。

この度、貴社のプロジェクトに関心を持たせていただきました。
私は{experience_level}として、以下のスキルを持っています：

【スキル】
{skills_list}

【実績】
- 複数のクライアント案件を成功させた経験あり
- 納期厳守、品質重視のポリシーで運営中
- クライアント満足度: 90%以上

【料金】
月額 ¥{target_income:,}程度でのご対応が可能です。

貴社のニーズに合わせてカスタマイズも可能ですので、
ぜひ一度ご相談いただけますでしょうか？

よろしくお願いいたします。

{name}
        """,

        "sns_twitter": """
🎯 副業で月{target_income_short}円を目指しています！

【スキル】{skills_short}

【実績】
✅ クライアント満足度 90%以上
✅ 納期遵守率 100%
✅ リピート率 80%以上

お仕事のご依頼はDMまでお気軽に！

#副業 #フリーランス #{first_skill}
        """,

        "sns_instagram": """
副業で稼ぐ方法 📱

こんにちは、{name}です！

私は{experience_level}として活動中です。

【得意分野】
{skills_bullet}

【実績】
📊 {achievement_count}件以上のプロジェクト完了
👥 クライアント満足度 90%以上
⏰ 納期遵守率 100%

あなたも副業で月{target_income_short}円を目指しませんか？

#副業 #在宅勤務 #{first_skill} #フリーランス #稼ぎ方
        """,

        "linkedin": """
Professional Profile

Current Focus: Freelancing in {skills_str}

Experience Level: {experience_level}

Key Skills:
{skills_list}

About Me:
Dedicated freelancer focused on delivering high-quality work within deadlines.
Experienced in working with diverse clients and adapting to various project requirements.

Target Monthly Income: ¥{target_income:,}

Client Satisfaction: 90%+
Project Success Rate: 100%

Looking for opportunities in: {first_skill}

Feel free to connect and let's explore opportunities together!
        """
    }

    def __init__(self, use_mock: bool = True):
        """
        Args:
            use_mock: True なら模擬テンプレートを使用（テスト用）
        """
        self.use_mock = use_mock
        self.generated_templates: Dict[str, GeneratedTemplate] = {}

    def generate_portfolio_template(self,
                                   profile: UserProfile,
                                   platform: str = "upwork") -> GeneratedTemplate:
        """ポートフォリオテンプレートを生成"""

        template_key = f"portfolio_{platform}"

        if self.use_mock:
            content = self._generate_from_mock(template_key, profile)
        else:
            content = self._generate_from_claude_api(template_key, profile)

        template = GeneratedTemplate(
            template_type="portfolio",
            content=content,
            platform=platform
        )

        self.generated_templates[f"portfolio_{platform}"] = template
        return template

    def generate_sales_email(self, profile: UserProfile) -> GeneratedTemplate:
        """営業メールテンプレートを生成"""

        if self.use_mock:
            content = self._generate_from_mock("sales_email", profile)
        else:
            content = self._generate_from_claude_api("sales_email", profile)

        template = GeneratedTemplate(
            template_type="sales_email",
            content=content,
            platform="email"
        )

        self.generated_templates["sales_email"] = template
        return template

    def generate_sns_posts(self, profile: UserProfile) -> Dict[str, GeneratedTemplate]:
        """SNS投稿テンプレートを生成"""

        platforms = ["twitter", "instagram", "linkedin"]
        templates = {}

        for platform in platforms:
            template_key = f"sns_{platform}"

            if self.use_mock:
                content = self._generate_from_mock(template_key, profile)
            else:
                content = self._generate_from_claude_api(template_key, profile)

            template = GeneratedTemplate(
                template_type="sns_post",
                content=content,
                platform=platform
            )

            templates[platform] = template
            self.generated_templates[f"sns_{platform}"] = template

        return templates

    def _generate_from_mock(self, template_type: str, profile: UserProfile) -> str:
        """模擬テンプレートを生成"""

        if template_type not in self.MOCK_TEMPLATES:
            return f"[{template_type}] テンプレートが見つかりません"

        template = self.MOCK_TEMPLATES[template_type]

        # プロフィール情報で置換
        skills_str = ", ".join(profile.skills)
        skills_list = "\n".join([f"• {skill}" for skill in profile.skills])
        skills_short = "、".join(profile.skills[:3])
        skills_bullet = "\n".join([f"📍 {skill}" for skill in profile.skills])

        first_skill = profile.skills[0] if profile.skills else "freelance"
        experience_level_jp = self._experience_to_jp(profile.experience_level)
        target_income_short = f"¥{profile.target_monthly_income // 10000}万"
        achievement_count = 10 + len(profile.skills) * 5

        content = template.format(
            name=profile.name,
            skills_str=skills_str,
            skills_list=skills_list,
            skills_short=skills_short,
            skills_bullet=skills_bullet,
            first_skill=first_skill,
            experience_level=experience_level_jp,
            target_income=profile.target_monthly_income,
            target_income_short=target_income_short,
            achievement_count=achievement_count,
            skill_1=profile.skills[0] if profile.skills else "freelance"
        )

        return content

    def _generate_from_claude_api(self, template_type: str, profile: UserProfile) -> str:
        """Claude API でテンプレートを生成（実装時）"""
        # TODO: Anthropic API を統合
        # 現在は模擬テンプレートを返す
        return self._generate_from_mock(template_type, profile)

    def _experience_to_jp(self, experience_level: ExperienceLevel) -> str:
        """経験レベルを日本語に変換"""
        return {
            ExperienceLevel.BEGINNER: "初心者",
            ExperienceLevel.INTERMEDIATE: "中級者",
            ExperienceLevel.ADVANCED: "上級者"
        }.get(experience_level, "フリーランサー")

    def edit_template(self, template_id: str, new_content: str) -> bool:
        """テンプレートを編集"""

        if template_id not in self.generated_templates:
            return False

        template = self.generated_templates[template_id]

        if not template.is_editable:
            return False

        template.content = new_content
        return True

    def export_template(self, template_id: str, format: str = "text") -> Optional[str]:
        """テンプレートをエクスポート"""

        if template_id not in self.generated_templates:
            return None

        template = self.generated_templates[template_id]

        if format == "text":
            return template.content
        elif format == "markdown":
            return f"# {template.template_type} ({template.platform})\n\n{template.content}"
        elif format == "html":
            return f"<div class='{template.template_type}'>\n{template.content}\n</div>"
        else:
            return template.content

    def get_all_generated_templates(self) -> Dict[str, GeneratedTemplate]:
        """生成されたすべてのテンプレートを取得"""
        return self.generated_templates

    def clear_generated_templates(self) -> bool:
        """生成されたテンプレートをクリア"""
        self.generated_templates.clear()
        return True

    def get_template_stats(self) -> Dict:
        """テンプレート統計を取得"""
        stats = {
            "total_generated": len(self.generated_templates),
            "by_type": {},
            "by_platform": {}
        }

        for template_id, template in self.generated_templates.items():
            # タイプ別
            if template.template_type not in stats["by_type"]:
                stats["by_type"][template.template_type] = 0
            stats["by_type"][template.template_type] += 1

            # プラットフォーム別
            if template.platform not in stats["by_platform"]:
                stats["by_platform"][template.platform] = 0
            stats["by_platform"][template.platform] += 1

        return stats
