from src import db

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)

payments_methods = db.Table(
    "payments_methods",
    db.Column("payment_method_id", db.Integer(), db.ForeignKey("payment_method.id")),
    db.Column("payment_id", db.Integer(), db.ForeignKey("payment.id")),
)
