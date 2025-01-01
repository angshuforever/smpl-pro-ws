# Import required libraries
import pandas as pd
from datetime import datetime
import os
import csv
from IPython.display import clear_output

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.monthly_budget = 0.0
        self.filename = 'expenses.csv'
        self.load_expenses()

    def validate_date(self, date_str):
        """Validate the date format YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_amount(self, amount_str):
        """Validate the expense amount"""
        try:
            amount = float(amount_str)
            return amount > 0
        except ValueError:
            return False

    def add_expense(self):
        """Take date, category, amount and description info as input. Make sure amount variable is a float
           variable because input function always produce string output.
           Store above info in a dictionary and then append to the expenses list variable in the parameter"""

        clear_output(wait=True)
        print("\n=== Add New Expense ===")

        # Get date
        while True:
            date = input("Enter date (YYYY-MM-DD): ")
            if self.validate_date(date):
                break
            print("Invalid date format. Please use YYYY-MM-DD")

        # Get category
        categories = ['Food', 'Transportation', 'Housing', 'Entertainment', 'Utilities', 'Other']
        print("\nAvailable categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        while True:
            try:
                choice = int(input("\nSelect category number: "))
                if 1 <= choice <= len(categories):
                    category = categories[choice - 1]
                    break
                print("Invalid choice. Please select a number from the list.")
            except ValueError:
                print("Please enter a valid number.")

        # Get amount
        while True:
            amount_str = input("Enter amount spent: ")
            if self.validate_amount(amount_str):
                amount = float(amount_str)
                break
            print("Invalid amount. Please enter a positive number.")

        # Get description
        while True:
            description = input("Enter description: ").strip()
            if description:
                break
            print("Description cannot be empty.")

        # Create and add expense
        expense = {
            'date': date,
            'category': category,
            'amount': amount,
            'description': description
        }
        self.expenses.append(expense)
        print("\nExpense added successfully!")

    def view_expenses(self):
        """ Implement a function that displays all recorded expenses.
            The function ensures that all required fields (date, category, amount, description) are present
            before displaying the expense. If no expenses are recorded, it informs the user.

            Required fields:
            - date: The date of the expense
            - category: The expense category
            - amount: The expense amount
            - description: A description of the expense
        """
        clear_output(wait=True)
        print("\n=== View Expenses ===")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        # Required fields for validation
        required_fields = ['date', 'category', 'amount', 'description']
        valid_expenses = []
        invalid_count = 0

        # Validate each expense record
        for expense in self.expenses:
            if all(field in expense for field in required_fields):
                valid_expenses.append(expense)
            else:
                invalid_count += 1
                print(f"Invalid expense record found: {expense}")

        if invalid_count > 0:
            print(f"\nFound {invalid_count} invalid expense records that will be skipped.")

        if not valid_expenses:
            print("No valid expenses to display.")
            return

        # Convert valid expenses to DataFrame
        df = pd.DataFrame(valid_expenses)
        df = df.sort_values(by='date')

        # Group by category and calculate total
        category_totals = df.groupby('category')['amount'].sum()

        print("\nExpense Details:")
        print("=" * 80)
        for index, row in df.iterrows():
            print(f"Date: {row['date']}")
            print(f"Category: {row['category']}")
            print(f"Amount: {row['amount']:.2f}")
            print(f"Description: {row['description']}")
            print("-" * 80)

        print("\nCategory-wise Totals:")
        print("=" * 40)
        for category, total in category_totals.items():
            print(f"{category}: {total:.2f}")
        print(f"\nTotal Expenses: {df['amount'].sum():.2f}")

    def set_budget(self):
        """Take an input from the user what is the amount to set for monthly budget store as a float variable."""
        clear_output(wait=True)
        print("\n=== Set Monthly Budget ===")

        while True:
            try:
                budget = float(input("Enter monthly budget amount: "))
                if budget > 0:
                    self.monthly_budget = budget
                    print(f"\nMonthly budget set to: {budget:.2f}")
                    break
                print("Budget must be greater than 0.")
            except ValueError:
                print("Please enter a valid number.")

    def track_budget(self):
        """
        Loop through your expenses list and fetch amount field
        Keep summing up amount field and store the final summed value to a variable - total_expenses
        Compare above total_expenses against budget variable
        if total_expenses > budget raise an alarm to the user - "Warning: You have exceeded your budget!"
        Else - You are within your budget, You have {budget - total_expenses} remaining."

        """



        clear_output(wait=True)
        print("\n=== Budget Tracking ===")

        if self.monthly_budget == 0:
            print("Monthly budget not set. Please set a budget first.")
            return

        total_expenses = sum(expense['amount'] for expense in self.expenses)
        remaining = self.monthly_budget - total_expenses

        print(f"Monthly Budget: {self.monthly_budget:.2f}")
        print(f"Total Expenses: {total_expenses:.2f}")
        print(f"Remaining: {remaining:.2f}")

        if remaining < 0:
            print("\n⚠️ WARNING: You have exceeded your budget!")
        elif remaining < (0.2 * self.monthly_budget):
            print("\n⚠️ WARNING: You're close to exceeding your budget!")
        else:
            print(f"\nYou are within your budget, You have {remaining:.2f} remaining.")

    def save_expenses(self):
        """Save expenses to CSV file"""
        try:
            with open(self.filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
                writer.writeheader()
                writer.writerows(self.expenses)
            print(f"\nExpenses saved successfully to {self.filename}")
            return True
        except Exception as e:
            print(f"Error saving expenses: {str(e)}")
            return False

    def load_expenses(self):
        """Load expenses from CSV file"""
        if not os.path.exists(self.filename):
            return

        try:
            df = pd.read_csv(self.filename)
            self.expenses = df.to_dict('records')
            print(f"Loaded {len(self.expenses)} expenses from {self.filename}")
        except Exception as e:
            print(f"Error loading expenses: {str(e)}")

    def display_menu(self):
        """Display the main menu"""
        menu = """
                === Personal Expense Tracker ===
                1. Add Expense
                2. View Expenses
                3. Set Monthly Budget
                4. Track Budget
                5. Save Expenses
                6. Exit
                """
        print(menu)

    def run(self):
        """ The interactive menu allows users to navigate through the options of adding an expense,
            viewing expenses, tracking their budget, saving expenses, or exiting the program.
            When exiting, it ensures that any newly added expenses are saved to the file."""
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.set_budget()
            elif choice == '4':
                self.track_budget()
            elif choice == '5':
                self.save_expenses()
            elif choice == '6':
                if self.save_expenses():
                    print("\nThank you for using Personal Expense Tracker!")
                    break
                else:
                    print("\nWould you like to exit without saving? (yes/no)")
                    if input().lower().startswith('y'):
                        break
            else:
                print("Invalid choice, please select a valid option.")

            input("\nPress Enter to continue...")
            clear_output(wait=True)


# Create and run the expense tracker
if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
