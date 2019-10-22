# db init
from flask_security.utils import hash_password

from src import Role, User, app, db
from src.models import Email
from src.models.Application import Application

db.drop_all()
db.create_all()

u = User(
    username="admin",
    active=True,
    name="admin 1",
    address="lol",
    country="e",
    city="zz",
    number="45445",
)
u2 = User(
    username="user1",
    active=True,
    name="user 1",
    address="lol",
    country="e",
    city="zz",
    number="47445",
)
u3 = User(
    username="user2",
    active=True,
    name="user 2",
    address="lol",
    country="e",
    city="zz",
    number="48445",
)
u.active = True

for a, u in enumerate([u, u2, u3]):
    e = Email(label=f"user{a}@host.com")
    e.is_primary = True
    e.receive_notifications = True
    u.email = e.label
    u.emails.append(e)

r = Role(name="admin")
r1 = Role(name="user")

u.roles = [r, r1]
u2.roles = [r1]
u3.roles = [r1]

apps = [Application(name=f"app_{str(x)}", user=u, enabled=True) for x in range(1, 5)]
apps2 = [Application(name=f"app_{str(x)}", user=u2, enabled=True) for x in range(1, 5)]

# apps[0].enabled = True
# apps[0].entrypoint = "foobar.py"
# apps[0].domain_name = "app1.com"

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
