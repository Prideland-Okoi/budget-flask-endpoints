import functools
from flask import Flask, request, jsonify, current_app, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import login_user, logout_user, login_required, current_user, LoginManager, UserMixin
from datetime import datetime, timedelta  


# Import the models
from models import db, User, UserProfile, Category, Transaction, Account, Budget, Currency, Report, Notification

# Create a Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize the models
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Create a decorator for parsing JSON requests
def json_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return make_response(jsonify({'message': 'Request must be JSON'}), 400)
        return f(*args, **kwargs)
    return decorated



# Create a route for updating a user profile
@app.route('/user/<int:user_id>/profile', methods=['PUT'])
@json_required
def update_user_profile(user_id):
    user_profile = UserProfile.query.filter_by(user_id=user_id).first()
    if user_profile is None:
        return make_response(jsonify({'message': 'User profile not found'}), 404)

    # Update the user profile with the JSON data from the request
    user_profile.first_name = request.json['first_name']
    user_profile.last_name = request.json['last_name']
    user_profile.phone_number = request.json['phone_number']

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with the updated user profile
    return jsonify({
        'id': user_profile.id,
        'user_id': user_profile.user_id,
        'profile_picture': user_profile.profile_picture,
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'phone_number': user_profile.phone_number
    })

# Create a route for deleting a user
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response(jsonify({'message': 'User not found'}), 404)

    # Delete the user from the database
    db.session.delete(user)

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with a success message
    return jsonify({'message': 'User deleted successfully'})

# Create a route for getting all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()

    # Return a JSON response with all the users
    return jsonify({
        'users': [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email
            } for user in users
        ]
    })

# Create a route for creating a new user
@app.route('/user', methods=['POST'])
@json_required
def create_user():
    # Get the user data from the JSON request
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    # Create a new user object
    user = User(username=username, email=email, password=password)

    # Save the new user to the database
    db.session.add(user)
    db.session.commit()

    # Return a JSON response with the new user's details
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })


# Create a route for updating a transaction
@app.route('/transaction/<int:transaction_id>', methods=['PUT'])
@json_required
def update_transaction(transaction_id):
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    if transaction is None:
        return make_response(jsonify({'message': 'Transaction not found'}), 404)

    # Update the transaction with the JSON data from the request
    transaction.transaction_date = request.json['transaction_date']
    transaction.description = request.json['description']
    transaction.category_id = request.json['category_id']
    transaction.amount = request.json['amount']
    transaction.is_income = request.json['is_income']

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with the updated transaction
    return jsonify({
        'id': transaction.id,
        'user_id': transaction.user_id,
        'transaction_date': transaction.transaction_date,
        'description': transaction.description,
        'category_id': transaction.category_id,
        'amount': transaction.amount,
        'is_income': transaction.is_income
    })

# Create a route for deleting a transaction
@app.route('/transaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    if transaction is None:
        return make_response(jsonify({'message': 'Transaction not found'}), 404)

    # Delete the transaction from the database
    db.session.delete(transaction)

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with a success message
    return jsonify({'message': 'Transaction deleted successfully'})

# Create a route for getting all transactions for a user
@app.route('/user/<int:user_id>/transactions', methods=['GET'])
def get_all_transactions_for_user(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    # Return a JSON response with all the transactions for the user
    return jsonify({
        'transactions': [
            {
                'id': transaction.id,
                'user_id': transaction.user_id,
                'transaction_date': transaction.transaction_date,
                'description': transaction.description,
                'category_id': transaction.category_id,
                'amount': transaction.amount,
                'is_income': transaction.is_income
            } for transaction in transactions
        ]
    })

# Create a route for creating a new transaction
@app.route('/transaction', methods=['POST'])
@json_required
def create_transaction():
    # Get the transaction data from the JSON request
    user_id = request.json['user_id']
    transaction_date = request.json['transaction_date']
    description = request.json['description']
    category_id = request.json['category_id']
    amount = request.json['amount']
    is_income = request.json['is_income']

    # Create a new transaction object
    transaction = Transaction(user_id=user_id, transaction_date=transaction_date, description=description, category_id=category_id, amount=amount, is_income=is_income)

    # Save the new transaction to the database
    db.session.add(transaction)
    db.session.commit()

    # Return a JSON response with the new transaction's details
    return jsonify({
        'id': transaction.id,
        'user_id': transaction.user_id,
        'transaction_date': transaction.transaction_date,
        'description': transaction.description,
        'category_id': transaction.category_id,
        'amount': transaction.amount,
        'is_income': transaction.is_income
    })

# Create a route for updating an account
@app.route('/account/<int:account_id>', methods=['PUT'])
@json_required
def update_account(account_id):
    account = Account.query.filter_by(id=account_id).first()
    if account is None:
        return make_response(jsonify({'message': 'Account not found'}), 404)

    # Update the account with the JSON data from the request
    account.account_name = request.json['account_name']
    account.account_type = request.json['account_type']
    account.balance = request.json['balance']

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with the updated account
    return jsonify({
        'id': account.id,
        'user_id': account.user_id,
        'account_name': account.account_name,
        'account_type': account.account_type,
        'balance': account.balance
    })

# Create a route for getting all accounts for a user
@app.route('/user/<int:user_id>/accounts', methods=['GET'])
def get_all_accounts_for_user(user_id):
    accounts = Account.query.filter_by(user_id=user_id).all()

    # Return a JSON response with all the accounts for the user
    return jsonify({
        'accounts': [
            {
                'id': account.id,
                'user_id': account.user_id,
                'account_name': account.account_name,
                'account_type': account.account_type,
                'balance': account.balance
            } for account in accounts
        ]
    })

# Create a route for creating a new account
@app.route('/account', methods=['POST'])
@json_required
def create_account():
    # Get the account data from the JSON request
    user_id = request.json['user_id']
    account_name = request.json['account_name']
    account_type = request.json['account_type']
    balance = request.json['balance']

    # Create a new account object
    account = Account(user_id=user_id, account_name=account_name, account_type=account_type, balance=balance)

    # Save the new account to the database
    db.session.add(account)
    db.session.commit()

    # Return a JSON response with the new account's details
    return jsonify({
        'id': account.id,
        'user_id': account.user_id,
        'account_name': account.account_name,
        'account_type': account.account_type,
        'balance': account.balance
    })

# Create a route for deleting an account
@app.route('/account/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = Account.query.filter_by(id=account_id).first()
    if account is None:
        return make_response(jsonify({'message': 'Account not found'}), 404)

    # Delete the account from the database
    db.session.delete(account)

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with a success message
    return jsonify({'message': 'Account deleted successfully'})

# Create a route for updating a budget
@app.route('/budget/<int:budget_id>', methods=['PUT'])
@json_required
def update_budget(budget_id):
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget is None:
        return make_response(jsonify({'message': 'Budget not found'}), 404)

    # Update the budget with the JSON data from the request
    budget.category = request.json['category']
    budget.budgeted_amount = request.json['budgeted_amount']

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with the updated budget
    return jsonify({
        'id': budget.id,
        'user_id': budget.user_id,
        'category': budget.category,
        'budgeted_amount': budget.budgeted_amount
    })

# Create a route for getting all budgets for a user
@app.route('/user/<int:user_id>/budgets', methods=['GET'])
def get_all_budgets_for_user(user_id):
    budgets = Budget.query.filter_by(user_id=user_id).all()

    # Return a JSON response with all the budgets for the user
    return jsonify({
        'budgets': [
            {
                'id': budget.id,
                'user_id': budget.user_id,
                'category': budget.category,
                'budgeted_amount': budget.budgeted_amount
            } for budget in budgets
        ]
    })

# Create a route for creating a new budget
@app.route('/budget', methods=['POST'])
@json_required
def create_budget():
    # Get the budget data from the JSON request
    user_id = request.json['user_id']
    category = request.json['category']
    budgeted_amount = request.json['budgeted_amount']

    # Create a new budget object
    budget = Budget(user_id=user_id, category=category, budgeted_amount=budgeted_amount)

    # Save the new budget to the database
    db.session.add(budget)
    db.session.commit()

    # Return a JSON response with the new budget's details
    return jsonify({
        'id': budget.id,
        'user_id': budget.user_id,
        'category': budget.category,
        'budgeted_amount': budget.budgeted_amount
    })

# Create a route for deleting a budget
@app.route('/budget/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget is None:
        return make_response(jsonify({'message': 'Budget not found'}), 404)

    # Delete the budget from the database
    db.session.delete(budget)

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with a success message
    return jsonify({'message': 'Budget deleted successfully'})

# Create a route for updating a currency
@app.route('/currency/<int:currency_id>', methods=['PUT'])
@json_required
def update_currency(currency_id):
    currency = Currency.query.filter_by(id=currency_id).first()
    if currency is None:
        return make_response(jsonify({'message': 'Currency not found'}), 404)

    # Update the currency with the JSON data from the request
    currency.code = request.json['code']
    currency.exchange_rate = request.json['exchange_rate']

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with the updated currency
    return jsonify({
        'id': currency.id,
        'code': currency.code,
        'exchange_rate': currency.exchange_rate
    })

# Create a route for getting all currencies
@app.route('/currencies', methods=['GET'])
def get_all_currencies():
    currencies = Currency.query.all()

    # Return a JSON response with all the currencies
    return jsonify({
        'currencies': [
            {
                'id': currency.id,
                'code': currency.code,
                'exchange_rate': currency.exchange_rate
            } for currency in currencies
        ]
    })

# Create a route for creating a new currency
@app.route('/currency', methods=['POST'])
@json_required
def create_currency():
    # Get the currency data from the JSON request
    code = request.json['code']
    exchange_rate = request.json['exchange_rate']

    # Create a new currency object
    currency = Currency(code=code, exchange_rate=exchange_rate)

    # Save the new currency to the database
    db.session.add(currency)
    db.session.commit()

    # Return a JSON response with the new currency's details
    return jsonify({
        'id': currency.id,
        'code': currency.code,
        'exchange_rate': currency.exchange_rate
    })

# Create a route for deleting a currency
@app.route('/currency/<int:currency_id>', methods=['DELETE'])
def delete_currency(currency_id):
    currency = Currency.query.filter_by(id=currency_id).first()
    if currency is None:
        return make_response(jsonify({'message': 'Currency not found'}), 404)

    # Delete the currency from the database
    db.session.delete(currency)

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with a success message
    return jsonify({'message': 'Currency deleted successfully'})

# Create a route for updating a report
@app.route('/report/<int:report_id>', methods=['PUT'])
@json_required
def update_report(report_id):
    report = Report.query.filter_by(id=report_id).first()
    if report is None:
        return make_response(jsonify({'message': 'Report not found'}), 404)

    # Update the report with the JSON data from the request
    report.report_date = request.json['report_date']
    report.income_total = request.json['income_total']
    report.expense_total = request.json['expense_total']
    report.balance = request.json['balance']

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with the updated report
    return jsonify({
        'id': report.id,
        'user_id': report.user_id,
        'report_date': report.report_date,
        'income_total': report.income_total,
        'expense_total': report.expense_total,
        'balance': report.balance
    })

# Create a route for getting all reports for a user
@app.route('/user/<int:user_id>/reports', methods=['GET'])
def get_all_reports_for_user(user_id):
    reports = Report.query.filter_by(user_id=user_id).all()

    # Return a JSON response with all the reports for the user
    return jsonify({
        'reports': [
            {
                'id': report.id,
                'user_id': report.user_id,
                'report_date': report.report_date,
                'income_total': report.income_total,
                'expense_total': report.expense_total,
                'balance': report.balance
            } for report in reports
        ]
    })

# Create a route for creating a new report
@app.route('/report', methods=['POST'])
@json_required
def create_report():
    # Get the report data from the JSON request
    user_id = request.json['user_id']
    report_date = request.json['report_date']
    income_total = request.json['income_total']
    expense_total = request.json['expense_total']
    balance = request.json['balance']

    # Create a new report object
    report = Report(user_id=user_id, report_date=report_date, income_total=income_total, expense_total=expense_total, balance=balance)

    # Save the new report to the database
    db.session.add(report)
    db.session.commit()

    # Return a JSON response with the new report's details
    return jsonify({
        'id': report.id,
        'user_id': report.user_id,
        'report_date': report.report_date,
        'income_total': report.income_total,
        'expense_total': report.expense_total,
        'balance': report.balance
    })

# Create a route for deleting a report
@app.route('/report/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    report = Report.query.filter_by(id=report_id).first()
    if report is None:
        return make_response(jsonify({'message': 'Report not found'}), 404)

    # Delete the report from the database
    db.session.delete(report)

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with a success message
    return jsonify({'message': 'Report deleted successfully'})


# Create a route for updating a notification
@app.route('/notification/<int:notification_id>', methods=['PUT'])
@json_required
def update_notification(notification_id):
    notification = Notification.query.filter_by(id=notification_id).first()
    if notification is None:
        return make_response(jsonify({'message': 'Notification not found'}), 404)

    # Update the notification with the JSON data from the request
    notification.message = request.json['message']
    notification.timestamp = request.json['timestamp']

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with the updated notification
    return jsonify({
        'id': notification.id,
        'user_id': notification.user_id,
        'message': notification.message,
        'timestamp': notification.timestamp
    })

# Create a route for getting all notifications for a user
@app.route('/user/<int:user_id>/notifications', methods=['GET'])
def get_all_notifications_for_user(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).all()

    # Return a JSON response with all the notifications for the user
    return jsonify({
        'notifications': [
            {
                'id': notification.id,
                'user_id': notification.user_id,
                'message': notification.message,
                'timestamp': notification.timestamp
            } for notification in notifications
        ]
    })

# Create a route for creating a new notification
@app.route('/notification', methods=['POST'])
@json_required
def create_notification():
    # Get the notification data from the JSON request
    user_id = request.json['user_id']
    message = request.json['message']
    timestamp = request.json['timestamp']

    # Create a new notification object
    notification = Notification(user_id=user_id, message=message, timestamp=timestamp)

    # Save the new notification to the database
    db.session.add(notification)
    db.session.commit()

    # Return a JSON response with the new notification's details
    return jsonify({
        'id': notification.id,
        'user_id': notification.user_id,
        'message': notification.message,
        'timestamp': notification.timestamp
    })

# Create a route for deleting a notification
@app.route('/notification/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notification = Notification.query.filter_by(id=notification_id).first()
    if notification is None:
        return make_response(jsonify({'message': 'Notification not found'}), 404)

    # Delete the notification from the database
    db.session.delete(notification)

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response with a success message
    return jsonify({'message': 'Notification deleted successfully'})

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
