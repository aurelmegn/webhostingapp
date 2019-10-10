# db init
from flask_security.utils import hash_password

from src.models.Application import Application
from src import db, User, Role, app

db.drop_all()
db.create_all()

u = User(username="admin", email="admin@mail.com", active=True)
u2 = User(username="user1", email="user1@mail.com", active=True)
u.active = True

r = Role(name="admin")
r1 = Role(name="user")

u.roles = [r, r1]
u2.roles = [r1]

apps = [Application(name=f"app_{str(x)}", user=u) for x in range(1, 10)]
apps2 = [Application(name=f"app_{str(x)}", user=u2) for x in range(1, 10)]

with app.app_context():
    u.password = hash_password("shift")
    u2.password = hash_password("shift")

# for a in apps:
#     db.session.add(a)

db.session.add(u)
db.session.commit()
