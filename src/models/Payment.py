from datetime import datetime

from src import db
from src.utils.HelperClass import AlchemySerializable


class PaymentMethod(db.Model, AlchemySerializable):
    id = db.Column(db.Integer(), primary_key=True)

    label = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())

    payments = db.relationship("Payment", backref="payment_method", lazy=False)


class Payment(db.Model, AlchemySerializable):
    id = db.Column(db.Integer(), primary_key=True)

    price = db.Column(db.Numeric(), unique=True, nullable=False)

    at = db.Column(db.DateTime(), default=datetime.utcnow())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())

    application_id = db.Column(
        db.Integer, db.ForeignKey("application.id"), nullable=False
    )
    payment_method_id = db.Column(
        db.Integer, db.ForeignKey("payment_method.id"), nullable=False
    )
    payment_plan_id = db.Column(
        db.Integer, db.ForeignKey("payment_plan.id"), nullable=False
    )


class PaymentPlan(db.Model, AlchemySerializable):
    id = db.Column(db.Integer(), primary_key=True)

    month_frequency = db.Column(db.Integer(), nullable=False)
    reduction = db.Column(db.Numeric(), default=0)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())

    payments = db.relationship("Payment", backref="payment_plan", lazy=True)
    # application_id = db.Column(db.Integer, db.ForeignKey("application.id"))
