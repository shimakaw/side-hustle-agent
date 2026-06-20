#!/usr/bin/env python3
"""
インタラクティブ実行スクリプト
ユーザーが情報を入力して、エージェントを実行
"""

import sys
import os
import json
from datetime import datetime

# パスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.main import SideHustleSupportAgent
from agents.profiler import ExperienceLevel, TimeCommitment


def print_header():
    """ヘッダーを表示"""
    print("\n" + "="*70)
    print("🎯 副業支援エージェント - インタラクティブモード")
    print("="*70)
    print("\nあなたの情報を入力してください。")
    print("（選択肢の場合は番号で選択）\n")


def get_name() -> str:
    """名前を入力"""
    while True:
        name = input("👤 お名前: ").strip()
        if name and len(name) <= 50:
            return name
        print("   ⚠️  名前を入力してください（50文字以内）")


def get_experience_level() -> ExperienceLevel:
    """経験レベルを選択"""
    print("\n📊 副業の経験レベル:")
    print("   1. 初心者（未経験）")
    print("   2. 中級者（1-3ヶ月経験）")
    print("   3. 上級者（3ヶ月以上経験）")

    while True:
        choice = input("   選択 (1-3): ").strip()
        if choice == "1":
            return ExperienceLevel.BEGINNER
        elif choice == "2":
            return ExperienceLevel.INTERMEDIATE
        elif choice == "3":
            return ExperienceLevel.ADVANCED
        print("   ⚠️  1-3 の番号で選択してください")


def get_skills() -> list:
    """スキルを入力"""
    print("\n🔧 スキル（カンマ区切りで3個まで入力）:")
    print("   例: python, web design, ライティング")

    while True:
        skills_input = input("   スキル: ").strip()
        if not skills_input:
            print("   ⚠️  スキルを入力してください")
            continue

        skills = [s.strip() for s in skills_input.split(",")][:10]

        if len(skills) == 0:
            print("   ⚠️  スキルが認識されませんでした")
            continue

        if all(len(s) > 0 and len(s) <= 30 for s in skills):
            return skills

        print("   ⚠️  各スキルは30文字以内にしてください")


def get_target_income() -> int:
    """目標月収を入力"""
    print("\n💰 目標月収（円）:")
    print("   例: 50000（5万円）、100000（10万円）")

    while True:
        try:
            income = int(input("   月収: ").strip())
            if 10000 <= income <= 10000000:
                return income
            print("   ⚠️  1万円～1000万円の範囲で入力してください")
        except ValueError:
            print("   ⚠️  数字で入力してください")


def get_time_commitment() -> TimeCommitment:
    """時間的余裕を選択"""
    print("\n⏰ 1週間に使える時間:")
    print("   1. 5～10時間（週末だけ）")
    print("   2. 10～20時間（かなり時間ある）")
    print("   3. 20時間以上（ほぼ専業）")

    while True:
        choice = input("   選択 (1-3): ").strip()
        if choice == "1":
            return TimeCommitment.PART_TIME
        elif choice == "2":
            return TimeCommitment.SEMI_FULL_TIME
        elif choice == "3":
            return TimeCommitment.FULL_TIME
        print("   ⚠️  1-3 の番号で選択してください")


def print_results(results: dict):
    """結果を表示"""
    print("\n" + "="*70)
    print("✅ 分析完了！")
    print("="*70)

    counseling = results.get('counseling', {})

    if 'error' not in counseling:
        # プロフィール
        profile = counseling.get('profile', {})
        print(f"\n📋 あなたのプロフィール")
        print(f"   名前: {profile.get('name')}")
        print(f"   スキル: {', '.join(profile.get('skills', []))}")
        print(f"   目標月収: ¥{profile.get('target_monthly_income'):,}")

        # 推奨副業
        opportunities = counseling.get('opportunities', [])
        if opportunities:
            print(f"\n🎯 あなたに最適な副業 TOP 3")
            for i, opp in enumerate(opportunities[:3], 1):
                print(f"\n   {i}. {opp['title']}")
                print(f"      マッチスコア: {opp['match_score']}%")
                print(f"      予想月収: ¥{opp['estimated_income']:,}")

        # ロードマップ
        if 'roadmap' in results:
            roadmap_data = results['roadmap'].get('roadmap', {})
            if 'opportunity' in roadmap_data:
                print(f"\n📅 実行ロードマップ")
                print(f"   推奨副業: {roadmap_data['opportunity']['title']}")

                phases = roadmap_data.get('phases', {})
                for phase_name, phase_data in phases.items():
                    print(f"\n   【{phase_name}】 ({phase_data['duration_weeks']}週間)")
                    for task in phase_data.get('tasks', []):
                        print(f"      ✓ {task}")

    print("\n" + "="*70)
    print("📝 次のステップ:")
    print("="*70)
    print(f"""
1. 結果ファイルを確認
   → results/session_*.json を確認

2. テンプレートを確認
   → results/templates_*/ フォルダのテンプレート

3. フィードバックを送信
   → GitHub Issues または Slack で報告

""")


def save_results(user_name: str, results: dict):
    """結果をファイルに保存"""
    # 出力ディレクトリを作成
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # タイムスタンプ
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # セッション結果を保存
    session_file = os.path.join(results_dir, f"session_{timestamp}.json")
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n💾 結果を保存しました:")
    print(f"   {session_file}")

    # テンプレートディレクトリを作成
    templates_dir = os.path.join(results_dir, f"templates_{timestamp}")
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)

    # テンプレートを保存
    templates = results.get('templates', {})
    for category, items in templates.items():
        if isinstance(items, dict):
            for platform, data in items.items():
                if 'content' in data:
                    file_name = f"{category}_{platform}.txt"
                    file_path = os.path.join(templates_dir, file_name)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(data['content'])

    print(f"   テンプレート: {templates_dir}/")

    # フィードバックフォームを作成
    feedback_file = os.path.join(results_dir, f"feedback_{timestamp}.json")
    feedback_template = {
        "user_name": user_name,
        "date": datetime.now().isoformat(),
        "rating": {
            "usability": "1-5で評価（1:低い、5:高い）",
            "accuracy": "提案の正確さ（1-5）",
            "templates": "テンプレートの質（1-5）"
        },
        "comments": {
            "what_was_good": "何がよかった？",
            "what_to_improve": "何を改善すべき？",
            "feature_requests": "欲しい機能は？"
        }
    }

    with open(feedback_file, 'w', encoding='utf-8') as f:
        json.dump(feedback_template, f, ensure_ascii=False, indent=2)

    print(f"   フィードバック: {feedback_file}")
    print(f"\n   💬 上記のフィードバックファイルを編集して、")
    print(f"      GitHub Issues で共有してください！")


def main():
    """メイン処理"""
    try:
        print_header()

        # ユーザー情報を入力
        name = get_name()
        experience_level = get_experience_level()
        skills = get_skills()
        target_income = get_target_income()
        time_commitment = get_time_commitment()

        print("\n" + "="*70)
        print("⏳ 分析中... （30秒程度かかります）")
        print("="*70)

        # エージェントを実行
        agent = SideHustleSupportAgent()
        results = agent.run_full_session(
            name=name,
            experience_level=experience_level,
            skills=skills,
            target_monthly_income=target_income,
            time_commitment=time_commitment
        )

        # 結果を表示
        print_results(results)

        # 結果を保存
        save_results(name, results)

        print("="*70)
        print("✅ 完了しました！")
        print("="*70)
        print("\n📌 次は GitHub Issues でフィードバックをお願いします！")
        print("   https://github.com/dejiina-university/side-hustle-agent/issues")

    except KeyboardInterrupt:
        print("\n\n⚠️  キャンセルされました")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
