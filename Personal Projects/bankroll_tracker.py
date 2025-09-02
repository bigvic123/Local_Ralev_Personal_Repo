import csv
from datetime import datetime, timedelta
import os
from typing import Optional

file_name = "poker_bankroll.csv"

bankroll = 0.0

club_names = [
    "SkylineGG",
    "Salt City",
    "Division One",
    "The Hangar Club",
    "Ti1ted",
    "Tilted Tavern",
]

club_file_dir = "club_balances"

DATETIME_FMT = "%Y-%m-%d %H:%M:%S"

def _format_amount(value: float) -> str:
    i = int(round(value))
    return str(i) if abs(value - i) < 1e-9 else f"{value:.2f}"

def _parse_amount(s: str) -> float:
    return float(s.strip().replace(",", "").replace("−", "-").replace("–", "-").replace("—", "-"))

def _parse_datetime(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    s = date_str.strip().replace("T", " ")
    for fmt in (DATETIME_FMT, "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None

def _get_club_filename(club: str) -> str:
    safe = club.replace(" ", "_").replace("/", "_")
    return os.path.join(club_file_dir, f"{safe}.csv")

def _initialise_club_files() -> None:
    if not os.path.exists(club_file_dir):
        os.makedirs(club_file_dir)
    for club in club_names:
        fn = _get_club_filename(club)
        if not os.path.exists(fn):
            with open(fn, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Balance", "Source", "Change"])
                writer.writerow([0, "Initial", 0])

def _load_club_balances() -> dict[str, float]:
    _initialise_club_files()
    balances: dict[str, float] = {}
    for club in club_names:
        fn = _get_club_filename(club)
        try:
            with open(fn, mode="r", newline="") as f:
                reader = csv.reader(f)
                next(reader, None)
                last_row = None
                for row in reader:
                    if row:
                        last_row = row
                balances[club] = float(last_row[0]) if last_row else 0.0
        except (FileNotFoundError, ValueError, IndexError):
            balances[club] = 0.0
    return balances

def _save_club_balance(club: str, new_balance: float, source: str) -> None:
    fn = _get_club_filename(club)
    _initialise_club_files()
    last_balance = 0.0
    if os.path.exists(fn):
        with open(fn, mode="r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and len(row) >= 1:
                    try:
                        last_balance = float(row[0])
                    except ValueError:
                        continue
    change = new_balance - last_balance
    with open(fn, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([_format_amount(new_balance), source, _format_amount(change)])

def manage_club_balances() -> None:
    while True:
        balances = _load_club_balances()
        print("\n--- Poker Club Balances ---")
        for idx, club in enumerate(club_names, start=1):
            print(f"{idx}. {club:<15}: ${balances[club]:.2f}")
        print("0. Return to Main Menu")
        choice = input(f"Select a club to update (0-{len(club_names)}): ").strip()
        if choice == "0":
            break
        if choice in {str(i) for i in range(1, len(club_names) + 1)}:
            club = club_names[int(choice) - 1]
            try:
                new_balance = float(input(f"Enter the NEW balance you want for {club}: "))
                print("What is the source of this update?")
                print("1. Play")
                print("2. Transaction")
                source_choice = input("Enter 1 or 2: ").strip()
                source_map = {"1": "Play", "2": "Transaction"}
                if source_choice not in source_map:
                    print("Invalid source choice. Please enter 1 or 2.")
                    continue
                source = source_map[source_choice]
                fn = _get_club_filename(club)
                last_balance = 0.0
                try:
                    with open(fn, mode="r", newline="") as f:
                        reader = csv.reader(f)
                        next(reader, None)
                        for row in reader:
                            if row and len(row) >= 1:
                                last_balance = float(row[0])
                except Exception:
                    pass
                change = new_balance - last_balance
                _save_club_balance(club, new_balance, source)
                print(f"{club} balance updated to ${new_balance:.2f} from {source}. The balance changed by ${change:+.2f}")
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")
        else:
            print("Invalid choice. Please try again.")

def _ensure_main_file():
    if not os.path.exists(file_name):
        open(file_name, "a").close()

def _iter_transactions():
    if not os.path.exists(file_name):
        return
    with open(file_name, mode="r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            if row[0].strip().lower() == "date":
                continue
            if len(row) >= 4:
                yield [row[0], row[1], row[2], row[3]]

if os.path.exists(file_name):
    try:
        for r in _iter_transactions():
            try:
                bankroll = _parse_amount(r[3])
            except Exception:
                continue
    except Exception:
        bankroll = 0.0
else:
    _ensure_main_file()

def update_bankroll(amount: float, category: str) -> None:
    global bankroll
    bankroll += amount
    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime(DATETIME_FMT),
            category,
            _format_amount(amount),
            _format_amount(bankroll),
        ])
    print(f"Updated Bankroll: ${bankroll:.2f}")

def view_alltime_profit_loss() -> None:
    if not os.path.exists(file_name):
        print("No transaction history found.")
        return
    categories = {
        "Micro-NLH": 0.0,
        "Mid-NLH": 0.0,
        "High Stakes": 0.0,
        "Bonus/Fee": 0.0,
        "PLO": 0.0,
        "2B-PLO": 0.0,
        "Tournament": 0.0,
        "Heads Up": 0.0,
        "Unknown": 0.0,
    }
    try:
        for row in _iter_transactions():
            if len(row) < 3:
                continue
            cat = row[1]
            if cat in categories:
                try:
                    categories[cat] += _parse_amount(row[2])
                except ValueError:
                    continue
    except Exception as e:
        print(f"Error reading transaction history: {e}")
        return
    print("\n--- All-Time Profit/Loss by Category ---")
    for category, total in categories.items():
        print(f"{category:<15}: ${total:.2f}")

def view_profit_loss_in_timeframe() -> None:
    if not os.path.exists(file_name):
        print("No transaction history found.")
        return
    try:
        days = int(input("Enter the number of days: "))
        hours = int(input("Enter the number of hours: "))
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return
    time_limit = datetime.now() - timedelta(days=days, hours=hours)
    total_profit_loss = 0.0
    try:
        for row in _iter_transactions():
            dt = _parse_datetime(row[0])
            if dt is None or dt < time_limit:
                continue
            try:
                total_profit_loss += _parse_amount(row[2])
            except ValueError:
                continue
    except Exception as e:
        print(f"Error reading transaction history: {e}")
        return
    print(f"\nNet Profit/Loss in the last {days} days and {hours} hours: ${total_profit_loss:.2f}")

def main() -> None:
    global bankroll
    while True:
        print("\n--- Poker Bankroll Tracker ---")
        print(f"Current Bankroll: ${bankroll:.2f}")
        print("1. Add/Subtract a Transaction")
        print("2. View Transaction History")
        print("3. Exit")
        print("4. View All-Time Profit/Loss by Category")
        print("5. View Profit/Loss in a Given Timeframe")
        print("6. Manage Poker Club Balances")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            try:
                amount = float(input("Enter the transaction amount (+ for win, - for loss): "))
                print("Transaction type options:")
                print("1. Micro-NLH")
                print("2. Mid-NLH")
                print("3. High Stakes")
                print("4. PLO")
                print("5. 2B-PLO")
                print("6. Tournament")
                print("7. Heads Up")
                print("8. Bonus/Fee")
                type_choice = input("Select transaction type (1-8): ")
                types = {
                    "1": "Micro-NLH",
                    "2": "Mid-NLH",
                    "3": "High Stakes",
                    "4": "PLO",
                    "5": "2B-PLO",
                    "6": "Tournament",
                    "7": "Heads Up",
                    "8": "Bonus/Fee",
                }
                category = types.get(type_choice, "Unknown")
                update_bankroll(amount, category)
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        elif choice == "2":
            rows = list(_iter_transactions()) or []
            print("\n--- Transaction History ---")
            for r in rows:
                print(",".join([r[0], r[1], r[2], r[3]]))
        elif choice == "3":
            print("Exiting the tracker.")
            break
        elif choice == "4":
            view_alltime_profit_loss()
        elif choice == "5":
            view_profit_loss_in_timeframe()
        elif choice == "6":
            manage_club_balances()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
