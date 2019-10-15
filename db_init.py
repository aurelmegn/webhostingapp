# db init
from flask_security.utils import hash_password

from src.models.Application import Application
from src import db, User, Role, app

db.drop_all()
db.create_all()

u = User(username="admin", email="admin@mail.com", active=True)
u2 = User(username="user1", email="user1@mail.com", active=True)
u3 = User(username="user2", email="user2@mail.com", active=True)
u.active = True

r = Role(name="admin")
r1 = Role(name="user")

u.roles = [r, r1]
u2.roles = [r1]
u3.roles = [r1]

apps = [Application(name=f"app_{str(x)}", user=u) for x in range(1, 10)]
apps2 = [Application(name=f"app_{str(x)}", user=u2) for x in range(1, 10)]

apps[0].enabled = True
apps[0].entrypoint = "foobar.py"
apps[0].domain_name = "app1.com"

with app.app_context():
    u.password = hash_password("shift")
    u2.password = hash_password("shift")
    u3.password = hash_password("shift")

# for a in apps:
#     db.session.add(a)

db.session.add(u)
db.session.add(u2)
db.session.add(u3)
db.session.commit()
