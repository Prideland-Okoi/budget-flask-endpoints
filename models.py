from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import LargeBinary
from flask_jwt_extended import create_access_token

db = SQLAlchemy()

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # Relationships
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    accounts = db.relationship('Account', backref='user', lazy=True)
    budgets = db.relationship('Budget', backref='user', lazy=True)
    
    def generate_access_token(self):
        return create_access_token(identity=self.id)
    
# Define the UserProfile model
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profile_picture = db.Column(db.LargeBinary(), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))

    # Create a one-to-one relationship between the User and UserProfile models
    user = db.relationship('UserProfile', backref='user', uselist=False)
    
# Category Model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

# Transaction Model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    # category = db.Column(db.String(80), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    is_income = db.Column(db.Boolean, nullable=False)  # True for income, False for expense
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
# Account Model
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_name = db.Column(db.String(80), nullable=False)
    account_type = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Float, nullable=False)

# Budget Model
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    budgeted_amount = db.Column(db.Float, nullable=False)

# Currency Model
class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)

# Report Model
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    report_date = db.Column(db.DateTime, nullable=False)
    income_total = db.Column(db.Float, nullable=False)
    expense_total = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)

# Notification Model
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
