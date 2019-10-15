from flask import render_template, Blueprint

blog_bp = Blueprint("blog", __name__, url_prefix="/blog")


@blog_bp.route("/")
def index():
    return render_template("default/blog.jinja")
