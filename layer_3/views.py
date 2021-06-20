from init import db
from models import Expense, User
import datetime

"""
    Functions that can be carried out by the User.
"""


def create_user(username, password, budget, income):
    new_user = User()
    new_user.username = username
    new_user.hash_password(password)
    new_user.budget = budget
    new_user.income = income
    db.session.add(new_user)
    db.session.commit()
    return new_user


def create_new_expense(username, item_name, category, amount, merchant):
    new_expense = Expense()
    new_expense.item_name = item_name
    new_expense.category = category
    new_expense.amount = amount
    new_expense.merchant = merchant
    new_expense.date_of_expense = datetime.datetime.now()
    new_expense.username = username
    db.session.add(new_expense)
    db.session.commit()
    return new_expense


def get_user(username):  # return User.query.filter_by(username=username).first()  # That shit fit be flask cause am.
    result = db.session.query(User).filter_by(username=username).first()
    return result


def get_expense(username, search_string):
    return db.session.query(Expense).filter_by(username=username).\
        filter(Expense.item_name.like("%" + search_string + "%")).all


def update_budget(username, budget):
    result = db.session.query(User).filter_by(username=username).update(budget)
    return result


def update_income(username, income):
    result = db.session.query(User).filter_by(username=username).update(income)
    return result


def get_monthly_total_expense_by_category(username, month):
    result = db.session.query(Expense.category.label("Category"), db.func.sum(Expense.amount)).\
        filter_by(username=username).group_by(Expense.category).where(Expense.date_month == month)
    return result


# Add percentages later..
def get_yearly_total_expense_by_category(username, year):
    result = db.session.query(Expense.category.label("Category"), db.func.sum(Expense.amount)). \
        filter_by(username=username).group_by(Expense.category).where(Expense.date_year == year)
    return result


