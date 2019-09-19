# db init
from flask_security.utils import hash_password

from src import db, User, Role, app

db.drop_all()
db.create_all()

u = User(username="admin", email="admin@mail.com")
u.active = True

r = Role(name="admin")
u.roles.append(r)

with app.app_context():
    u.password = hash_password("shift")

    db.session.add(u)
    db.session.commit()
