import requests
import json
url = "http://127.0.0.1:5000/"


class Expense:

    def __init__(self, item_name: str, category: str, amount: float, merchant: str, username: str):
        self._item_name = item_name
        self._category = category
        self._amount = amount
        self._merchant = merchant
        self._username = username
        user_info = {"item_name": self._item_name, "category": self._category, "amount": self._amount,
                     "merchant": self._merchant}
        requests.post(url + "/User/<username>/Expense", json=user_info)

    @property
    def item_name(self):
        return self._item_name

    @item_name.setter
    def item_name(self, item):
        self._item_name = item

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        self._category = new_category

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, new_amount):
        self._amount = new_amount

    @property
    def merchant(self):
        return self._merchant

    @merchant.setter
    def merchant(self, new_merchant):
        self._merchant = new_merchant

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, user_name):
        self._username = user_name



