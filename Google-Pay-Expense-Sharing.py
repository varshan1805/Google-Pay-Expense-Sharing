# G-Pay Project.py
# Developed by: Varshan Raj
# Description: Interactive console-based expense sharing system (sample demo users included)
# Sample users: Ram, Krish, Senthil, Pooja
# Run: python "G-Pay Project.py"

class ExpenseSharing:
    def __init__(self):
        # Positive = others owe them, Negative = they owe others.
        self.balances = {}

    def add_expense(self, payer, amount, participants, split_type="equal", split_values=None):
        if amount <= 0 or not participants:
            print("⚠️ Invalid expense. Please check the amount or participants.")
            return

        n = len(participants)
        shares = {}

        # Equal split
        if split_type == "equal":
            share = round(amount / n, 2)
            for p in participants:
                shares[p] = share

        # Percent split
        elif split_type == "percent" and split_values:
            total_percent = sum(split_values.values())
            if total_percent == 0:
                print("⚠️ Percent values sum to 0. Falling back to equal split.")
                share = round(amount / n, 2)
                for p in participants:
                    shares[p] = share
            else:
                for p in participants:
                    percent = split_values.get(p, 0)
                    shares[p] = round((percent / total_percent) * amount, 2)

        # Exact split
        elif split_type == "exact" and split_values:
            total_share = sum(split_values.values())
            if total_share == 0:
                print("⚠️ Exact values sum to 0. Falling back to equal split.")
                share = round(amount / n, 2)
                for p in participants:
                    shares[p] = share
            else:
                if abs(total_share - amount) > 0.01:
                    print("⚠️ Adjusting exact amounts slightly to match total.")
                scale = amount / total_share if total_share != 0 else 1.0
                for p in participants:
                    shares[p] = round(split_values.get(p, 0) * scale, 2)
        else:
            print("⚠️ Invalid split type or missing data.")
            return

        # Update balances
        for person, share in shares.items():
            self.balances[person] = self.balances.get(person, 0) - share
        self.balances[payer] = self.balances.get(payer, 0) + amount

    def show_balances(self):
        print("\n💰 Current Balances:")
        if not self.balances:
            print("No records yet. Add an expense to begin.")
            return
        for person, balance in self.balances.items():
            if balance > 0:
                print(f"✅ {person} should receive ₹{round(balance, 2)}")
            elif balance < 0:
                print(f"❌ {person} owes ₹{abs(round(balance, 2))}")
            else:
                print(f"⚖️ {person} is settled up.")
        print("-------------------------------")

    def settle_up(self):
        debtors, creditors = [], []
        for name, balance in self.balances.items():
            if balance < 0:
                debtors.append([name, -balance])
            elif balance > 0:
                creditors.append([name, balance])

        debtors.sort(key=lambda x: x[1])
        creditors.sort(key=lambda x: x[1])

        i = j = 0
        settlements = []
        while i < len(debtors) and j < len(creditors):
            debtor, debt_amt = debtors[i]
            creditor, cred_amt = creditors[j]
            amount = round(min(debt_amt, cred_amt), 2)
            settlements.append(f"💸 {debtor} → {creditor}: ₹{amount}")
            debtors[i][1] -= amount
            creditors[j][1] -= amount
            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1
        return settlements

def demo_populate(system):
    # Pre-fill sample users and some example expenses for quick demo
    # Users: Ram, Krish, Senthil, Pooja
    system.add_expense("Ram", 1200, ["Ram", "Krish", "Senthil"], "equal")
    system.add_expense("Krish", 1800, ["Ram", "Krish", "Senthil", "Pooja"], "equal")
    system.add_expense("Senthil", 500, ["Ram", "Senthil"], "exact", {"Ram":200, "Senthil":300})
    system.add_expense("Pooja", 760, ["Krish", "Pooja"], "percent", {"Krish":60, "Pooja":40})

def input_float(prompt):
    while True:
        try:
            val = float(input(prompt))
            return val
        except ValueError:
            print("Please enter a valid number. Try again.")

def main_menu():
    system = ExpenseSharing()

    # Auto-populate demo data
    demo_populate(system)
    print("Demo data loaded: Ram, Krish, Senthil, Pooja (sample expenses pre-filled).")

    while True:
        print("\n========= G-Pay Project (Console Demo) =========")
        print("1) Add a new expense")
        print("2) Show balances")
        print("3) Show suggested settlements")
        print("4) Reset demo data")
        print("5) Exit")
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            payer = input("Who paid? ").strip()
            amount = input_float("Enter total amount (₹): ")
            parts = input("Enter participants (comma-separated): ")
            participants = [p.strip() for p in parts.split(",") if p.strip()]
            print("Split types: equal | percent | exact")
            split_type = input("Enter split type: ").strip().lower()
            split_values = None
            if split_type in ("percent", "exact"):
                split_values = {}
                print("Enter split values for each participant:")
                for p in participants:
                    v = input_float(f"  {p}'s value (percent or exact amount): ")
                    split_values[p] = v
            system.add_expense(payer, amount, participants, split_type, split_values)
            print("✅ Expense added.")

        elif choice == "2":
            system.show_balances()

        elif choice == "3":
            settlements = system.settle_up()
            if settlements:
                print("\n🤝 Suggested Settlements:")
                for s in settlements:
                    print(s)
            else:
                print("Everyone is settled up!")

        elif choice == "4":
            system = ExpenseSharing()
            demo_populate(system)
            print("Demo data reset.")

        elif choice == "5":
            print("Goodbye — thanks for trying the demo!")
            break
        else:
            print("Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main_menu()
