import PySimpleGUI as sg
from layer_2 import User, Expense


def welcome_page():
    layout = [[sg.Text("Welcome to Expense Tracker")],
              [sg.Text("Are you a new or an existing user?")],
              [sg.Button("Yes", key="Yes"), sg.Button("No", key="No")]]
    window = sg.Window(title="Expense Tracker", layout=layout, margins=(200, 200), element_justification="centre",
                       text_justification="centre")
    while True:
        event, values = window.read()
        window.close()
        if event == "Yes":
            new_user_authentication_page()
        if event == "No":
            old_user_authentication_page()
        if event == sg.WIN_CLOSED:
            break


def new_user_authentication_page():
    layout = [[sg.Text("Enter username")],
              [sg.InputText(key="username")],
              [sg.Text("Enter password")],
              [sg.InputText(key="password")],
              [sg.Button("Submit", key="Submit"), sg.Button("Cancel", key="Cancel")]]
    window = sg.Window(title="Expense Tracker", layout=layout, margins=(200, 200), element_justification="centre",
                       text_justification="centre")
    while True:
        event, values = window.read()
        window.close()
        if event == "Submit":
            user_name = str(values["username"])
            pass_word = str(values["password"])
            user = User.User(username=user_name, password=pass_word)
            welcome_user(user)
        if event == "Cancel":
            welcome_page()
        if event == sg.WIN_CLOSED:
            break


def old_user_authentication_page():
    layout = [[sg.Text("Enter username")],
              [sg.InputText(key="username")],
              [sg.Text("Enter password")],
              [sg.InputText(key="password")],
              [sg.Button("Submit", key="Submit"), sg.Button("Cancel", key="Cancel")]]
    window = sg.Window(title="Expense Tracker", layout=layout, margins=(200, 200), element_justification="centre",
                       text_justification="centre")
    while True:
        event, values = window.read()
        window.close()
        if event == "Submit":
            user_name = str(values["username"])
            pass_word = str(values["password"])
            user = User.User(username=user_name, password=pass_word)
            success = user.get_existing_user()["response"]
            if success:
                old_user = user
            else:
                x = True
                while x:
                    event, values = window.read()
                    user_name = str(values["username"])
                    pass_word = str(values["password"])
                    user = User.User(username=user_name, password=pass_word)
                    success = user.get_existing_user()["response"]
                    if success:
                        x = False
                old_user = user
            print("Retrieve new user from the database")
            print("Authenticating user")
            print("Hold user data in memory")
            welcome_user(old_user)
            if event == "No":
                welcome_page()
            if event == sg.WIN_CLOSED:
                break


def welcome_user(user):
    layout = [[sg.Text("Welcome " + user.username)],
              [sg.Button("OK", key="OK"), sg.Button("Cancel", key="Cancel")]]
    window = sg.Window(title="Expense Tracker", layout=layout, margins=(200, 200), element_justification="centre",
                       text_justification="centre")
    while True:
        event, values = window.read()
        window.close()
        if event == "OK":
            income_page(user)
        if event == "Cancel":
            welcome_page()
        if event == sg.WIN_CLOSED:
            break


def income_page(user):
    layout = [[sg.Text("What is your monthly income?")],
              [sg.Text("Only enter new values if it is your first time or if your income has changed.")],
              [sg.InputText(key="income")],
              [sg.Text("What is your savings this month by percentage?")],
              [sg.Text("Just enter figures and round up to 2decimal if needed e.g. 50.50")],
              [sg.InputText(key="savings")],
              [sg.Button("Submit", key="Submit"), sg.Button("Cancel", key="Cancel")]]
    window = sg.Window(title="Expense Tracker", layout=layout, margins=(200, 200), element_justification="centre",
                       text_justification="centre")
    while True:
        event, values = window.read()
        window.close()
        if event == "Submit":
            income = float(values["income"])
            savings = float(values["savings"])
            user.update_income(income)
            user.initial_monthly_budget(savings)
            expense_page(user)
        if event == "Cancel":
            expense_page(user)
        if event == sg.WIN_CLOSED:
            break


def expense_page(user):
    layout = [[sg.Text("What did you buy?")],
              [sg.InputText(key="item_name")],
              [sg.Text("Select a category for the expense")],
              [sg.InputText(key="category")],
              [sg.Text("Enter amount")],
              [sg.InputText(key="amount")],
              [sg.Text("Enter merchants name")],
              [sg.InputText(key="merchant")],
              [sg.Button("Submit", key="Submit"), sg.Button("Cancel", key="Cancel")]]
    window = sg.Window(title="Expense Tracker", layout=layout, margins=(200, 200), element_justification="c",
                       text_justification="centre")
    while True:
        event, values = window.read()
        window.close()
        if event == "Submit":
            item_name = values["item_name"]
            category = values["category"]
            amount = values["amount"]
            merchant = values["merchant"]
            expense = Expense.Expense(item_name=item_name, category=category,
                                      amount=amount, merchant=merchant, username=user.username)
            print("Use user data to create an entry in the expense table and fill in the entries.")
            remaining_budget_page(user, expense)
        if event == "Cancel":
            remaining_budget_page(user, 0)
        if event == sg.WIN_CLOSED:
            break


def remaining_budget_page(user, expense):
    layout = [[sg.Text("Your budget is remaining " + str(user.update_budget(expense)))],
              [sg.Button("OK", key="OK"), sg.Button("Cancel", key="Cancel")]]
    window = sg.Window(title="Expense Tracker", layout=layout, margins=(200, 200), element_justification="c",
                       text_justification="centre")
    while True:
        event, values = window.read()
        window.close()
        if event == "OK":
            welcome_page()
        if event == "Cancel":
            welcome_page()
        if event == sg.WIN_CLOSED:
            break


if __name__ == "__main__":
    welcome_page()
