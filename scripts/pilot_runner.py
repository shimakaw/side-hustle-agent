#!/usr/bin/env python3
"""
パイロット運用スクリプト
5ユーザーでの試験運用
"""

import sys
import os
import json
from datetime import datetime

# パスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.main import SideHustleSupportAgent
from agents.profiler import ExperienceLevel, TimeCommitment


class PilotRunner:
    """パイロット運用管理"""

    # パイロットユーザーサンプル
    PILOT_USERS = [
        {
            "id": "P001",
            "name": "山田太郎",
            "experience_level": ExperienceLevel.BEGINNER,
            "skills": ["python", "data analysis"],
            "target_monthly_income": 50000,
            "time_commitment": TimeCommitment.PART_TIME,
            "description": "未経験からPythonでデータ分析副業を目指す"
        },
        {
            "id": "P002",
            "name": "鈴木花子",
            "experience_level": ExperienceLevel.INTERMEDIATE,
            "skills": ["web design", "ui design"],
            "target_monthly_income": 100000,
            "time_commitment": TimeCommitment.SEMI_FULL_TIME,
            "description": "デザイン経験を活かしてフリーランス化"
        },
        {
            "id": "P003",
            "name": "佐藤次郎",
            "experience_level": ExperienceLevel.BEGINNER,
            "skills": ["writing", "content creation"],
            "target_monthly_income": 75000,
            "time_commitment": TimeCommitment.PART_TIME,
            "description": "ブログとSNS運用で副業化"
        },
        {
            "id": "P004",
            "name": "田中美咲",
            "experience_level": ExperienceLevel.ADVANCED,
            "skills": ["consulting", "business strategy"],
            "target_monthly_income": 200000,
            "time_commitment": TimeCommitment.SEMI_FULL_TIME,
            "description": "業界知識を活かしたコンサル副業"
        },
        {
            "id": "P005",
            "name": "伊藤健太",
            "experience_level": ExperienceLevel.INTERMEDIATE,
            "skills": ["video editing", "animation"],
            "target_monthly_income": 80000,
            "time_commitment": TimeCommitment.PART_TIME,
            "description": "動画編集スキルで映像制作副業"
        }
    ]

    def __init__(self, output_dir: str = "pilot_results"):
        self.output_dir = output_dir
        self.results = []
        self.feedback = []

        # 出力ディレクトリを作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

    def run_pilot_for_user(self, user_info: dict) -> dict:
        """個別ユーザーのパイロット実行"""

        print(f"\n{'='*60}")
        print(f"👤 パイロットユーザー: {user_info['name']} ({user_info['id']})")
        print(f"📝 {user_info['description']}")
        print(f"{'='*60}")

        agent = SideHustleSupportAgent()

        try:
            # フルセッション実行
            session_results = agent.run_full_session(
                name=user_info['name'],
                experience_level=user_info['experience_level'],
                skills=user_info['skills'],
                target_monthly_income=user_info['target_monthly_income'],
                time_commitment=user_info['time_commitment']
            )

            # 結果をまとめる
            result = {
                "user_id": user_info['id'],
                "name": user_info['name'],
                "status": "SUCCESS",
                "timestamp": datetime.now().isoformat(),
                "counseling": session_results.get('counseling', {}),
                "templates_generated": len(session_results.get('templates', {})),
                "platforms_analyzed": 3,
                "roadmap_generated": "roadmap" in session_results
            }

            return result

        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            return {
                "user_id": user_info['id'],
                "name": user_info['name'],
                "status": "FAILED",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    def run_all_pilots(self) -> list:
        """全パイロットユーザーで実行"""

        print("\n" + "="*60)
        print("🚀 パイロット運用開始")
        print("="*60)
        print(f"対象ユーザー数: {len(self.PILOT_USERS)}")
        print(f"開始時刻: {datetime.now().isoformat()}")

        for i, user_info in enumerate(self.PILOT_USERS, 1):
            print(f"\n[{i}/{len(self.PILOT_USERS)}]", end=" ")

            result = self.run_pilot_for_user(user_info)
            self.results.append(result)

            # 結果を表示
            if result['status'] == 'SUCCESS':
                print(f"✅ {result['name']}: 成功")
                print(f"   推奨機会: {result['counseling'].get('opportunities', [{}])[0].get('title', 'N/A')}")
            else:
                print(f"❌ {result['name']}: 失敗")

        print("\n" + "="*60)
        print("✅ パイロット運用完了")
        print("="*60)

        return self.results

    def generate_pilot_report(self) -> dict:
        """パイロット運用レポート生成"""

        successful = [r for r in self.results if r['status'] == 'SUCCESS']
        failed = [r for r in self.results if r['status'] == 'FAILED']

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_users": len(self.results),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": round(len(successful) / len(self.results) * 100, 1) if self.results else 0,
            "details": {
                "successful_users": [
                    {
                        "id": r['user_id'],
                        "name": r['name'],
                        "templates": r.get('templates_generated', 0),
                        "roadmap": r.get('roadmap_generated', False)
                    }
                    for r in successful
                ],
                "failed_users": [
                    {
                        "id": r['user_id'],
                        "name": r['name'],
                        "error": r.get('error', 'Unknown error')
                    }
                    for r in failed
                ]
            }
        }

        return report

    def save_results(self):
        """結果をファイルに保存"""

        report = self.generate_pilot_report()

        # レポートを保存
        report_path = os.path.join(self.output_dir, "pilot_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n📊 パイロットレポート: {report_path}")

        # 詳細結果を保存
        results_path = os.path.join(self.output_dir, "pilot_results.json")
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f"📋 詳細結果: {results_path}")

        return report

    def collect_feedback(self):
        """フィードバック収集用テンプレートを生成"""

        feedback_template = {
            "feedback_form": [
                {
                    "question": "エージェントは何度も使いたいと思いましたか？",
                    "type": "scale",
                    "scale": "1-5",
                    "field": "usability"
                },
                {
                    "question": "提案された副業は適切でしたか？",
                    "type": "scale",
                    "scale": "1-5",
                    "field": "accuracy"
                },
                {
                    "question": "生成されたテンプレートは実際に使えると思いましたか？",
                    "type": "scale",
                    "scale": "1-5",
                    "field": "template_quality"
                },
                {
                    "question": "エージェントの応答速度は満足できるものでしたか？",
                    "type": "scale",
                    "scale": "1-5",
                    "field": "performance"
                },
                {
                    "question": "改善してほしい点は何ですか？",
                    "type": "text",
                    "field": "improvements"
                },
                {
                    "question": "その他のコメント・フィードバック",
                    "type": "text",
                    "field": "comments"
                }
            ]
        }

        feedback_path = os.path.join(self.output_dir, "feedback_form.json")
        with open(feedback_path, 'w', encoding='utf-8') as f:
            json.dump(feedback_template, f, ensure_ascii=False, indent=2)

        print(f"📝 フィードバック形式: {feedback_path}")

    def print_summary(self):
        """サマリーを表示"""

        report = self.generate_pilot_report()

        print("\n" + "="*60)
        print("📊 パイロット運用 最終レポート")
        print("="*60)

        print(f"\n✅ 成功: {report['successful']}/{report['total_users']} ({report['success_rate']}%)")
        print(f"❌ 失敗: {report['failed']}/{report['total_users']}")

        if report['details']['successful_users']:
            print("\n【成功したユーザー】")
            for user in report['details']['successful_users']:
                print(f"  • {user['name']} ({user['id']})")
                print(f"    - テンプレート生成: {user['templates']}個")
                print(f"    - ロードマップ: {'✅' if user['roadmap'] else '❌'}")

        if report['details']['failed_users']:
            print("\n【失敗したユーザー】")
            for user in report['details']['failed_users']:
                print(f"  • {user['name']} ({user['id']})")
                print(f"    - エラー: {user['error']}")

        print("\n" + "="*60)
        print("📋 次のステップ:")
        print("  1. フィードバック収集")
        print("  2. 改善点の実装")
        print("  3. 本番環境へのデプロイ")
        print("="*60 + "\n")


def main():
    """メイン実行"""

    try:
        # パイロットランナーを初期化
        runner = PilotRunner(output_dir="pilot_results")

        # 全パイロット実行
        runner.run_all_pilots()

        # 結果を保存
        runner.save_results()

        # フィードバック形式を生成
        runner.collect_feedback()

        # サマリーを表示
        runner.print_summary()

    except Exception as e:
        print(f"\n❌ パイロット実行エラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
