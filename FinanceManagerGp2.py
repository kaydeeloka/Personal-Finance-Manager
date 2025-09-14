#Finance Manager Group 2
import datetime #to import date data information
import json #to save data in a file
import os
import fire #to use CLI in program
from tabulate import tabulate #to create a table
import matplotlib.pyplot as plt #to create graph

#define data file path
DATA_FILE = "financial_data.json"

#function to load data file
def load_data(data_file):
    if os.path.exists(data_file):
        #read existing data from file
        with open(data_file, 'r') as file:
            loaded_data = json.load(file)
            #ensure 'budget' is always a dictionary
            if 'budget' not in loaded_data or not isinstance(loaded_data['budget'], dict):
                loaded_data['budget'] = {}
            return loaded_data
    else:
        #if file doesn't exist, initialize with empty data structure
        return {'transactions': [], 'budget': {}}

#function to save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

#function to calculate balance
def calculate_balance(transactions):
    total_income = sum(trans['amount'] for trans in transactions if trans['type'] == 'income')
    total_expenses = sum(trans['amount'] for trans in transactions if trans['type'] == 'expense')
    return total_income - total_expenses

data = load_data(DATA_FILE) #load existing data from file

#create class FinanceManager with various features
class FinanceManager:
    #function to add new income information
    def add_income(self):
        source = input("\nEnter income source (personal saving/salary/others): ")
        #declare source for the income
        if source in ["personal saving", "salary", "others"]:
            amount = float(input("Enter income amount: ₩"))
            #get date information
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            #append new income transaction to the data
            data['transactions'].append({
                'date': date,
                'amount': amount,
                'category': source,
                'type': 'income'
            })
            current_balance = calculate_balance(data['transactions'])
            print(f"Income added successfully. Your new balance is ₩{current_balance}\n")
            save_data(data)
        else:
            print("Invalid source.\n")
    
    #function to add new expense information
    def add_expense(self):
        category = input("\nEnter expense category (food/shopping/health/transport/bills/others): ")
         #declare category for expenses
        if category in ["food", "shopping", "health", "transport", "bills", "others"]:
            amount = float(input("Enter expense amount: ₩"))
            #get date information
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            #append new expense transaction to the data
            data['transactions'].append({
                'date': date,
                'amount': amount,
                'category': category,
                'type': 'expense'
            })
            current_balance = calculate_balance(data['transactions'])
            print(f"Expense added successfully. Your new balance is ₩{current_balance}\n")
            #ensure the 'budget' key exists
            if 'budget' not in data:
                data['budget'] = {}
            #check if the expense exceeds the budget for the specified category
            if category in data['budget']:
                budget_limit = data['budget'][category]
                if abs(amount) > budget_limit:
                    exceeded_amount = abs(amount) - budget_limit
                    print(f"Warning: Expense exceeds budget for {category} by ₩{exceeded_amount}\n")
            save_data(data)
        else:
            print("Invalid category.\n")
    
    #function to create a budget
    def create_budget(self):
        category = input("\nEnter your category (food/shopping/health/transport/bills/others): ")
        if category in ["food", "shopping", "health", "transport", "bills", "others"]:
            #ensure the 'budget' key exists
            if 'budget' not in data:
                data['budget'] = {}
            budget_limit = float(input("Enter your budget: ₩"))
            data['budget'][category] = budget_limit
            save_data(data)
            print(f"Budget created successfully. Budget for {category} set to: ₩{budget_limit}\n")
        else:
            print("Invalid category.\n")
    
    #function to delete a transaction
    def delete_transaction(self):
        transaction_type = input("\nEnter transaction type to be deleted (income/expense): ")
        if transaction_type == "income":
            headers_income = ["No.","Date", "Source", "Amount(₩)"]
            income_data = []
            print("\nIncome:")
            income_transactions = [trans for trans in data['transactions'] if trans['type'] == 'income']
            for idx, trans in enumerate(income_transactions, start=1):
                income_data.append([idx, trans['date'], trans['category'], trans['amount']])
            print(tabulate(income_data, headers=headers_income, tablefmt="fancy_grid"))

            if not income_transactions:
                print("No incomes available for deletion.\n")
                return

            try:
                index = int(input("\nEnter the index of the income to be deleted: "))
                index_income = [i for i, trans in enumerate(data['transactions']) if trans['type'] == 'income'][index - 1]
                confirmation = input("Are you sure you want to delete this income? (yes/no): ")
                if confirmation.lower() in ['yes', 'y']:
                    deleted_trans = data['transactions'].pop(index_income)
                    save_data(data)
                    current_balance = calculate_balance(data['transactions'])
                    print(f"Income {deleted_trans.get('category')} with amount {deleted_trans.get('amount', 0)} deleted successfully. \nYour new balance is {current_balance}.\n")
                else:
                    print("Deletion canceled.\n")
            except (IndexError, ValueError):
                print("Invalid index.Please enter a valid index.\n")

        elif transaction_type == "expense":
            headers_expense = ["No.", "Date", "Category", "Amount(₩)"]
            expense_data = []
            print("\nExpense:")
            expense_transactions = [trans for trans in data['transactions'] if trans['type'] == 'expense']
            for idx, trans in enumerate(expense_transactions, start=1):
                expense_data.append([idx, trans['date'], trans['category'], trans['amount']])
            print(tabulate(expense_data, headers=headers_expense, tablefmt="fancy_grid"))

            if not expense_transactions:
                print("No expenses available for deletion.\n")
                return

            try:
                index = int(input("\nEnter the index of the expense to be deleted: "))
                index_expense = [i for i, trans in enumerate(data['transactions']) if trans['type'] == 'expense'][index - 1]
                confirmation = input("Are you sure you want to delete this expense? (yes/no): ")
                if confirmation.lower() in ['yes', 'y']:
                    deleted_trans = data['transactions'].pop(index_expense)
                    save_data(data)
                    current_balance = calculate_balance(data['transactions'])
                    print(f"Expense {deleted_trans.get('category')} with amount {deleted_trans.get('amount', 0)} deleted successfully. \nYour new balance is {current_balance}.\n")
                else:
                    print("Deletion canceled.\n")
            except (IndexError, ValueError):
                print("Invalid index.\n")
        else:
            print("Invalid transaction type.\n")
    
    #function to delete a budget
    def delete_budget(self):
        headers_budget = ["Category", "Budget Limit(₩)"]
        budget_data = []
        print("\nBudget:")
        for idx, (budget_category, budget_limit) in enumerate(data['budget'].items(), start=1):
            budget_data.append([idx, budget_category, budget_limit])
        print(tabulate(budget_data, headers=headers_budget, tablefmt="fancy_grid"))
            
        if not data['budget']:
            print("No budget categories available for deletion.\n")
            return
        
        try:
            index = int(input(f"\nEnter the index of the budget category to be deleted: "))
            category_to_delete = list(data['budget'].keys())[index - 1]
            confirmation = input(f"Are you sure you want to delete the {category_to_delete} category? (yes/no): ")
            if confirmation.lower() == 'yes':
                del data['budget'][category_to_delete]
                save_data(data)
                print(f"Budget for {category_to_delete} deleted successfully.\n")
            else:
                print("Deletion canceled.\n")
        except (IndexError, ValueError):
            print("Invalid index.\n")
    
    #function to view transaction history
    def view_transaction(self):
        headers_income = ["Date", "Source", "Amount(₩)"]
        income_data = []
        print("\nTransaction History:")
        print("\nIncome:")
        for trans in data['transactions']:
            if trans['type'] == 'income':
                income_data.append([trans['date'], trans['category'], trans['amount']])
        print(tabulate(income_data, headers=headers_income, tablefmt="fancy_grid"))

        headers_expense = ["Date", "Category", "Amount(₩)"]
        expense_data = []
        print("\nExpense:")
        for trans in data['transactions']:
            if trans['type'] == 'expense':
                expense_data.append([trans['date'], trans['category'], trans['amount']])
        print(tabulate(expense_data, headers=headers_expense, tablefmt="fancy_grid"))
        print("\n")
    
    #function to check budget limits
    def check_budget(self):
        headers_budget = ["Category", "Budget Limit(₩)"]
        budget_data = []
        print("\nBudget:")
        for budget_category, budget_limit in data['budget'].items():
            budget_data.append([budget_category, budget_limit])
        print(tabulate(budget_data, headers=headers_budget, tablefmt="fancy_grid"))
        print("\n")

    #function to display a financial summary with data visualization
    def summary(self):
        #information for overview
        total_income = sum(trans['amount'] for trans in data['transactions'] if trans['type'] == 'income')
        total_expenses = sum(trans['amount'] for trans in data['transactions'] if trans['type'] == 'expense')
        current_savings = total_income - total_expenses

        labels_summary = ["Income", "Expenses", "Current \n Balance"]
        values_summary = [total_income, abs(total_expenses), current_savings]

        #information for expenses and income categories
        transactions = data['transactions']

        #combine transactions with the same category
        combined_income = {}
        combined_expense = {}

        for trans in transactions:
            category = trans['category']
            amount = trans['amount']
            if trans['type'] == 'income':
                combined_income[category] = combined_income.get(category, 0) + amount
            else:
                combined_expense[category] = combined_expense.get(category, 0) + abs(amount)

        #create a figure with subplots
        fig, axs = plt.subplots(2, 2, figsize=(15, 15))

        #plot pie chart for income categories
        axs[0, 0].pie(list(combined_income.values()), labels=list(combined_income.keys()), autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        axs[0, 0].axis('equal')  #equal aspect ratio ensures that pie is drawn as a circle.
        axs[0, 0].set_title('Income Categories\n', fontsize=14, fontweight='bold')

        axs[0, 1].pie(list(combined_expense.values()), labels=list(combined_expense.keys()), autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        axs[0, 1].axis('equal')  #equal aspect ratio ensures that pie is drawn as a circle.
        axs[0, 1].set_title('Expenses Categories\n', fontsize=14, fontweight='bold')

        #plot horizontal bar chart for expense summary
        bars_expense = axs[1, 0].barh(labels_summary, values_summary, color=['green', '#ffa600', '#58508d'])
        axs[1, 0].set_xlabel('Amount (₩)')
        axs[1, 0].set_ylabel('')
        axs[1, 0].set_title('\n\nFinance Overview', fontsize=14, fontweight='bold')

        #add annotations in the center of the bars for expenses
        for bar, value in zip(bars_expense, values_summary):
            if value != 0:
                axs[1, 0].text(value / 2, bar.get_y() + bar.get_height() / 2, f'{value:.2f} ₩', ha='center', va='center', color='black')

        #plot budget information
        axs[1, 1].axis('off')  #turn off axis for this subplot
        axs[1, 1].text(0.1, 0.9, "Budget(₩) :", fontsize=14, fontweight='bold')

        for i, (category, budget_limit) in enumerate(data['budget'].items(), start=1):
            axs[1, 1].text(0.1, 0.9 - i * 0.1, f"  {category}: ₩{budget_limit}", fontsize=12)

        plt.show()
    
    #function to generate a financial report
    def report(self, start_date=None, end_date=None, category=None):
        headers_count = ["Category", "Count", "Total(₩)"]
        
        #filter transactions based on optional parameters
        filtered_transactions = data['transactions']
        if category:
            filtered_transactions = [trans for trans in filtered_transactions if trans['category'] == category]

        #get counts and totals for income and expenses
        count_income = sum(1 for trans in filtered_transactions if trans['type'] == 'income')
        total_income = sum(trans['amount'] for trans in filtered_transactions if trans['type'] == 'income')
        count_expenses = sum(1 for trans in filtered_transactions if trans['type'] == 'expense')
        total_expenses = sum(trans['amount'] for trans in filtered_transactions if trans['type'] == 'expense')
        current_saving = total_income - total_expenses

        #display the information using tabulate
        print("\nFinancial Report\n")
        data_report = [
            ["Income", count_income, total_income], ["Expenses", count_expenses, total_expenses]
            ]
        print(tabulate(data_report, headers=headers_count, tablefmt="fancy_grid"))
        print(f"Current balance : ₩{current_saving} ")

        #display counts and totals by category for incomes
        categories_income = ["personal saving", "salary", "others"]
        category_data_income = []

        for category_income in categories_income:
            category_incomes = [trans for trans in filtered_transactions if trans['type'] == 'income' and trans['category'] == category_income]
            count_category_incomes = len(category_incomes)
            total_category_incomes = sum(trans["amount"] for trans in category_incomes)
            
            category_data_income.append([category_income.capitalize(), count_category_incomes, total_category_incomes])

        #display counts and total by category for incomes
        print("\nIncome:")
        headers_category_income = ["Source", "Count", "Total(₩)"]
        print(tabulate(category_data_income, headers=headers_category_income, tablefmt="pretty"))

        #display counts and totals by category for expenses
        categories_expense = ["food", "shopping", "health", "transport", "others"]
        category_data_expense = []

        for category_expense in categories_expense:
            category_expenses = [trans for trans in filtered_transactions if trans['type'] == 'expense' and trans['category'] == category_expense]
            count_category_expenses = len(category_expenses)
            total_category_expenses = sum(trans["amount"] for trans in category_expenses)
            category_data_expense.append([category_expense.capitalize(), count_category_expenses, total_category_expenses])

        #display counts and total by category for expenses
        print("\nExpense:")
        headers_category_expense = ["Category", "Count", "Total(₩)"]
        print(tabulate(category_data_expense, headers=headers_category_expense, tablefmt="pretty"))

        #budget warnings
        budget_warnings = []

        for trans in filtered_transactions:
            if trans['type'] == 'expense':
                category = trans['category']
                amount = abs(trans['amount'])
                budget_limit = data['budget'].get(category, None)
                if budget_limit is not None and amount > budget_limit:
                    exceeded_amount = amount - budget_limit
                    budget_warnings.append([category.capitalize(), f"₩{exceeded_amount}"])

        #print all budget warnings
        headers_budget_warnings = ["Category", "Exceeded Amount"]
        print("\nBudget Exceed:")
        print(tabulate(budget_warnings, headers=headers_budget_warnings, tablefmt="pretty"))
        print("\n")


if __name__ == "__main__":
    fire.Fire(FinanceManager)