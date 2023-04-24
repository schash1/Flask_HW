from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from blog.models import User
from blog.views.auth import auth_app

auth = Blueprint("auth", __name__, url_prefix="/auth", static_folder="../static")


@auth_app.route("/login/", methods=["GET", "POST"], endpoint="index")
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    if not username:
        return render_template("login.html", error="username not passed")

    user = User.query.filter_by(username=username).one_or_none()
    if user is None:
        return render_template("login.html", error=f"no user {username!r} found")

    login_user(user)
    return redirect(url_for("index"))


@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@auth_app.route("/secret/")
@login_required
def secret_view():
    return "Super secret data"
