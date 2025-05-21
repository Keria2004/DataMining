from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Tên người dùng đã tồn tại.")
            return redirect("/register")

        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash("Đăng ký thành công. Vui lòng đăng nhập.")
        return redirect("/login")

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
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