from flask import url_for, request
from flask_admin.menu import MenuLink
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from src import app, admin, db

from src.models.User import User
from src.models.Application import Application
from src.models.Role import Role

from flask_admin.contrib.sqla import ModelView
from flask_admin import helpers as admin_helpers


class Default(ModelView):
    can_view_details = True
    can_create = False
    # can_edit = False
    can_delete = False
    column_exclude_list = [
        "password",
        "created_at",
        "updated_at",
        "last_login_at",
        "current_login_ip",
        "current_login_at",
        "last_login_ip",
        "login_count",
        "confirmed_at",
    ]
    create_modal = True
    edit_modal = True
    can_export = True
    form_excluded_columns = ["username", "email", "password", *column_exclude_list]

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
                )

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        if current_user.is_authenticated:
            # permission denied
            abort(403)
        else:
            # login
            return redirect(url_for('security.login', next=request.url))


from flask_admin.contrib.sqla import ModelView

admin.add_view(Default(User, db.session))
admin.add_view(Default(Role, db.session))
admin.add_view(Default(Application, db.session))

with app.app_context():
    admin.add_link(MenuLink(name='Dashboard', url=url_for('dashboard')))
    admin.add_link(MenuLink(name='Logout', url=url_for('security.logout')))
