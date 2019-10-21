from datetime import datetime

from src import db
from src.utils.HelperClass import AlchemySerializable


class PaymentMethod(db.Model, AlchemySerializable):
    id = db.Column(db.Integer(), primary_key=True)

    label = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())


class Payment(db.Model, AlchemySerializable):
    id = db.Column(db.Integer(), primary_key=True)

    price = db.Column(db.Numeric(), unique=True, nullable=False)

    at = db.Column(db.DateTime(), default=datetime.utcnow())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())

    method = db.relationship(
        "PaymentMethod",
        secondary="payments_methods",
        backref=db.backref("payments", lazy="dynamic"),
    )

    payment_plan_id = db.Column(
        db.Integer, db.ForeignKey("payment_plan.id"), nullable=False
    )


class PaymentPlan(db.Model, AlchemySerializable):
    id = db.Column(db.Integer(), primary_key=True)

    month_frequency = db.Column(db.Integer(), nullable=False)
    is_current_plan = db.Column(db.Boolean(), default=True)
    next_payment = db.Column(db.DateTime(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())

    payments = db.relationship("Payment", backref="payment_plan", lazy=True)
    application_id = db.Column(db.Integer, db.ForeignKey("application.id"))
