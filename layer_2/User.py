import requests
import json
url = "http://127.0.0.1:5000/"


class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.budget = 0
        self.income = 0
        user_info = {"username": self.username, "password": self.password, "budget": self.budget,
                     "income": self.income}
        requests.post(url + "/User", json=user_info)

    def get_existing_user(self):
        user_info = json.loads(requests.get(url + '/User' + self.username + '/' + self.password).text)
        return user_info

    # @property
    # def username(self):
    #     return self.username
    #
    # @username.setter
    # def username(self, name):
    #     self.username = name
    #
    # @property
    # def password(self):
    #     return self.password
    #
    # @password.setter
    # def password(self, passw):
    #     self.password = passw
    #
    # @property
    # def budget(self):
    #     return self.budget
    #
    def initial_monthly_budget(self, savings):
        new_budget = self.income - ((savings/100) * self.income)
        self.budget = new_budget
        user_info = {"budget": self.budget}
        requests.post(url + '/User/' + self.username + '/budget', json=user_info)
    #
    # @property
    # def income(self):
    #     return self.income
    #
    # @income.setter
    # def income(self, new_income):
    #     self.income = new_income

    def update_budget(self, expense=0):
        print(type(expense))
        print("user budget: " + str(expense))
        self.budget -= float(expense)
        print(type(expense))
        user_info = {"budget": self.budget}
        requests.patch(url + '/User/' + self.username + '/budget', json=user_info)
        return self.budget

    def update_income(self, income):
        self.income = income
        user_info = {"income": self.income}
        requests.patch(url + '/User/' + self.username + '/income', json=user_info)

