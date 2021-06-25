import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from init import db
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.inspection import inspect


class Serializer(object):
    """Class for serializing SQLAlchemy objects into dicts."""

    @staticmethod
    def is_primitive(obj):
        return type(obj) in (int, float, str, bool)

    def serialize(self):
        fields = inspect(self).attrs.keys()
        return {c: getattr(self, c) for c in fields if Serializer.is_primitive(getattr(self, c))}

    @staticmethod
    def serialize_list(list_obj):
        return [m.serialize() for m in list_obj]


class Expense(db.Model, Serializer):
    __tablename__ = "expense_table"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(1024), nullable=False)
    amount = db.Column(db.Float)
    merchant = db.Column(db.String(128))
    date_of_expense = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    username = db.Column(db.String(32), db.ForeignKey('users_table.username'), nullable=False)

    @hybrid_property
    def date_month(self):
        return self.date_of_expense.month

    @hybrid_property
    def date_year(self):
        return self.date_of_expense.year

    def __repr__(self):
        return f'Secret Word: {self.secret_word} Game Score: {self.game_score} Game Status: {self.game_won}'


class User(db.Model, Serializer):
    __tablename__ = "users_table"
    __table_args__ = {"extend_existing": True}
    username = db.Column(db.String(32), primary_key=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    income = db.Column(db.Float, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    expenses = db.relationship('Expense', backref='game', lazy=True)
    total_expense = db.column_property(db.select([db.func.sum(Expense.amount)]).scalar_subquery().where(Expense.username == username))

    def hash_password(self, password):
        self.hashed_password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def __repr__(self):
        return f'Username: {self.username}'


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    # User.__table__.drop(db.engine)
    # Expense.__table__.drop(db.engine)
