
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("data.json")

def load_data():
    if not DATA_FILE.exists():
        return {"habits": [], "logs": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def list_habits(data):
    if not data["habits"]:
        print("등록된 습관이 없습니다.")
        return
    print("=== 현재 습관 목록 ===")
    for idx, habit in enumerate(data["habits"], start=1):
        print(f"{idx}. {habit}")

def add_habit(data):
    name = input("추가할 습관 이름을 입력하세요: ").strip()
    if not name:
        print("이름이 비어 있습니다.")
        return
    if name in data["habits"]:
        print("이미 존재하는 습관입니다.")
        return
    data["habits"].append(name)
    save_data(data)
    print(f"'{name}' 습관이 추가되었습니다.")

def delete_habit(data):
    list_habits(data)
    if not data["habits"]:
        return
    try:
        idx = int(input("삭제할 번호를 입력하세요: "))
        habit = data["habits"].pop(idx - 1)
    except (ValueError, IndexError):
        print("잘못된 번호입니다.")
        return
    for day in list(data["logs"].keys()):
        if habit in data["logs"][day]:
            data["logs"][day].remove(habit)
    save_data(data)
    print(f"'{habit}' 습관이 삭제되었습니다.")

def log_today(data):
    today = str(date.today())
    if today not in data["logs"]:
        data["logs"][today] = []
    list_habits(data)
    if not data["habits"]:
        return
    print("오늘 완료한 습관의 번호를 공백으로 구분해 입력하세요. (예: 1 3)")
    raw = input("> ").strip()
    if not raw:
        print("입력이 없습니다.")
        return
    done_idxs = set()
    for token in raw.split():
        try:
            done_idxs.add(int(token))
        except ValueError:
            print(f"무시된 입력: {token}")
    done_habits = []
    for idx in done_idxs:
        if 1 <= idx <= len(data["habits"]):
            done_habits.append(data["habits"][idx - 1])
    data["logs"][today] = done_habits
    save_data(data)
    print(f"{today} 기록이 저장되었습니다.")

def show_stats(data):
    if not data["logs"]:
        print("아직 기록이 없습니다.")
        return
    counts = {h: 0 for h in data["habits"]}
    for day, habits in data["logs"].items():
        for h in habits:
            counts[h] = counts.get(h, 0) + 1
    print("=== 통계 (총 완료 횟수) ===")
    for h, c in counts.items():
        print(f"{h}: {c}회 완료")

def main():
    data = load_data()
    menu = """
=== HabitTrackerCLI ===
1. 습관 목록 보기
2. 습관 추가
3. 습관 삭제
4. 오늘 기록하기
5. 통계 보기
0. 종료
선택: """
    while True:
        choice = input(menu).strip()
        if choice == "1":
            list_habits(data)
        elif choice == "2":
            add_habit(data)
        elif choice == "3":
            delete_habit(data)
        elif choice == "4":
            log_today(data)
        elif choice == "5":
            show_stats(data)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
