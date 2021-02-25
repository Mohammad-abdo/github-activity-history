import os
import random
import subprocess
import sys
from datetime import date, timedelta, time, datetime

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

START_YEAR = 2021
END_YEAR = 2025

USERNAME = "Mohammad-abdo"
EMAIL = "sdm800884@gmail.com"

COMMIT_MESSAGES = [
    "Update documentation and code comments",
    "Fix minor formatting and syntax issues",
    "Refactor internal utility functions",
    "Optimize data processing performance",
    "Update project dependencies and config",
    "Add test cases and assertions",
    "Fix edge case handling in helper methods",
    "Code cleanup and style improvements",
    "Implement core logic updates",
    "Enhance error handling and logging",
    "Restructure project module files",
    "Minor tweak to algorithm efficiency",
]

def generate_commits():
    current_date = date(START_YEAR, 1, 1)
    end_date = date(END_YEAR, 12, 31)
    
    total_commits = 0
    total_days = (end_date - current_date).days + 1
    
    print(f"[*] Starting natural GitHub commit history generator...")
    print(f"[*] Date range: {current_date} -> {end_date} ({total_days} days)")
    print(f"[*] Committer: {USERNAME} <{EMAIL}>")
    print(f"[*] Year 2026 will NOT be touched!")
    print("-" * 55)

    activity_file = "activity.txt"
    if not os.path.exists(activity_file):
        with open(activity_file, "w", encoding="utf-8") as f:
            f.write("# Contribution Log\n")
        subprocess.run(["git", "add", activity_file], check=True)

    in_break = 0
    current_year = current_date.year
    year_commits = 0

    env = os.environ.copy()

    while current_date <= end_date:
        if current_date.year != current_year:
            print(f"[+] Finished Year {current_year} -> Commits: {year_commits} (Total so far: {total_commits})")
            current_year = current_date.year
            year_commits = 0

        weekday = current_date.weekday() # 0 = Monday, 6 = Sunday
        is_weekend = weekday in (5, 6)

        # Occasional natural breaks (3-6 days off)
        if in_break > 0:
            in_break -= 1
            current_date += timedelta(days=1)
            continue
        elif random.random() < 0.015:
            in_break = random.randint(2, 5)
            current_date += timedelta(days=1)
            continue

        # Decide whether today has commits
        # Weekdays: ~85% active, Weekends: ~40% active
        active_chance = 0.40 if is_weekend else 0.85
        if random.random() > active_chance:
            current_date += timedelta(days=1)
            continue

        # Commit volume distribution for natural color shades:
        tier = random.random()
        if is_weekend:
            num_commits = random.randint(1, 3)
        else:
            if tier < 0.35:
                num_commits = random.randint(1, 2)
            elif tier < 0.80:
                num_commits = random.randint(3, 5)
            else:
                num_commits = random.randint(6, 8)

        # Generate commits throughout daytime
        for _ in range(num_commits):
            hour = random.randint(9, 22)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_dt = datetime.combine(current_date, time(hour, minute, second))
            iso_date = commit_dt.strftime("%Y-%m-%dT%H:%M:%S")

            with open(activity_file, "a", encoding="utf-8") as f:
                f.write(f"[{iso_date}] {random.choice(COMMIT_MESSAGES)}\n")

            env["GIT_AUTHOR_DATE"] = iso_date
            env["GIT_COMMITTER_DATE"] = iso_date

            msg = random.choice(COMMIT_MESSAGES)

            subprocess.run([
                "git",
                "-c", f"user.name={USERNAME}",
                "-c", f"user.email={EMAIL}",
                "commit",
                "-a",
                "-m", f"{msg} ({iso_date})",
                "--quiet"
            ], env=env, check=True)

            total_commits += 1
            year_commits += 1

        current_date += timedelta(days=1)

    print(f"[+] Finished Year {current_year} -> Commits: {year_commits} (Total: {total_commits})")
    print("=" * 55)
    print(f"[SUCCESS] All backdated commits successfully created!")
    print(f"[STATS] Grand total commits: {total_commits}")
    print(f"[PROTECTION] 2026 remains completely untouched.")
    print("=" * 55)

if __name__ == "__main__":
    generate_commits()
