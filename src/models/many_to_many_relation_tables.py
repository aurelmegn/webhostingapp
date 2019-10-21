from src import db

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)

applications_payments_plans = db.Table(
    "applications_payments_plans",
    db.Column("is_current_plan", db.Boolean(), default=True),
    db.Column("payment_plan_id", db.Integer(), db.ForeignKey("payment_plan.id")),
    db.Column("application_id", db.Integer(), db.ForeignKey("application.id")),
)
