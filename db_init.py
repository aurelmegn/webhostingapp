# db init
from flask_security.utils import hash_password

from src.models.Application import Application
from src import db, User, Role, app

db.drop_all()
db.create_all()

u = User(username="admin", email="admin@mail.com")
u.active = True

r = Role(name="admin")
r1 = Role(name="user")
u.roles.append(r)
u.roles.append(r1)

apps = [Application(name=f"app_{str(x)}") for x in range(1, 10)]
with app.app_context():
    u.password = hash_password("shift")

db.session.add(u)
db.session.commit()
