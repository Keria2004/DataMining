from flask import Blueprint, render_template, request, redirect, flash, session
from app.firebase_user import add_user, validate_user, get_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if get_user(username):
            flash("Tên người dùng đã tồn tại.")
            return redirect("/register")

        add_user(username, password)
        flash("Đăng ký thành công. Vui lòng đăng nhập.")
        return redirect("/login")

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if validate_user(username, password):
            session["username"] = username
            flash("Đăng nhập thành công.")
            return redirect("/")
        else:
            flash("Sai tài khoản hoặc mật khẩu.")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Đã đăng xuất.")
    return redirect("/login")
