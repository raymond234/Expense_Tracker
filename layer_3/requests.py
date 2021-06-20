import logging
from datetime import datetime
from sqlalchemy import exc
import sqlalchemy
from flask import jsonify, request, make_response, g
from init import app
import views
from models import User
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


@app.route("/")
def index():
    return "Welcome to Expense Tracker!"


@app.route("/User", methods=['POST', 'GET'])
def create_get_user():
    user_info = request.json
    if request.method == 'POST':
        try:
            username = user_info["username"]
            password = user_info["password"]
            budget = user_info["budget"]
            income = user_info["income"]
            if User.query.filter_by(username=username).first() is not None:
                return make_response(jsonify(response="Welcome " + username + ". " + "Please enter your password."),
                                     402)
            if username is None or password is None:
                return make_response(jsonify(response="Please enter a valid username or password"), 405)

            views.create_user(username=username, password=password, budget=budget, income=income)
            return make_response(jsonify(response='OK'), 201)
        except sqlalchemy.exc.InvalidRequestError:
            return make_response(jsonify(error='Bad request'), 400)
    if request.method == 'GET':
        username = user_info["username"]
        new_user = views.get_user(username=username)
        return jsonify(new_user.serialize())


@auth.verify_password
def verify_password(username, password):
    user = views.get_user(username)
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


# Scared I didn't use a get request. Hope this works.
@app.route('/User/<username>')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.route('/User/<username>/Expense', methods=['POST'])
def create_expense(username):
    # Check out the dictionaries returning stuff here out at the end of the day.
    user_info = request.json
    item_name = user_info["item_name"]
    category = user_info["category"]
    amount = user_info["amount"]
    merchant = user_info["merchant"]
    logging.info(f"User logged in as: {username}")
    if request.method == 'POST':
        try:
            views.create_new_expense(username=username, item_name=item_name, category=category, amount=amount,
                                     merchant=merchant)  # How is this parameter supposed to be set?
            return make_response(jsonify(response='OK'), 201)
        except sqlalchemy.exc.InvalidRequestError:
            return make_response(jsonify(error='Bad request'), 400)


@app.route('/User/<username>/budget', methods=['PATCH'])
def update_budget(username):
    print("I landed here b")
    user_info = request.json
    print(user_info)
    print(username)
    budget = user_info["budget"]
    print(budget)
    if budget is not None:
        try:
            budget = {"budget": user_info["budget"]}
            views.update_income(username, budget)
            return jsonify(response='OK')
        except (sqlalchemy.exc.InvalidRequestError, KeyError):
            return make_response(jsonify(error='Bad request'), 400)


@app.route('/User/<username>/income', methods=['PATCH'])
def update_income(username):

    user_info = request.json
    print(user_info)
    print(username)
    income = user_info["income"]
    print(income)
    if income is not None:
        try:
            income = {"income": user_info["income"]}
            views.update_income(username, income)
            return jsonify(response='OK')
        except (sqlalchemy.exc.InvalidRequestError, KeyError):
            return make_response(jsonify(error='Bad request'), 400)


@app.route('/User/<username>/Expense/expense', methods=['GET'])
def get_expense(username):
    user_info = request.json
    search_string = user_info["search_string"]
    if request.method == 'GET':
        old_expense = views.get_expense(username=username, search_string=search_string)
        return jsonify(old_expense.serialize())


@app.route('/User/<username>/<month>', methods=['GET'])
def get_monthly_expense_breakdown(username, month):
    logging.info(f'User with username {username} is checking monthly ratings.')
    return jsonify(views.get_monthly_total_expense_by_category(username, month))


@app.route('/User/<username>/<year>', methods=['GET'])
def get_yearly_expense_breakdown(username, year):
    logging.info(f'User with username {username} is checking monthly ratings.')
    return jsonify(views.get_monthly_total_expense_by_category(username, year))
