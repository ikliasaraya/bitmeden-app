from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, login_required, logout_user
from app.models import db, Business

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing = Business.query.filter_by(email=email).first()

        if existing:
            flash("E-posta zaten kayıtlı.", "error")
            return redirect(url_for("auth.register"))
        else:
            record = Business(name= name, email= email)
            record.set_password(password)
            db.session.add(record)
            db.session.commit()
            login_user(record)
            flash("Kayıt işlemi başarılı", "success")
            return redirect(url_for("dashboard.index"))
    else:
       return render_template("register.html")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        record = Business.query.filter_by(email=email).first()
        if record and record.check_password(password):
            login_user(record)
            return redirect(url_for("dashboard.index"))

        else:
            flash("E-posta veya şifre yanlış!","error")
            return redirect(url_for("auth.login"))
    else:
        return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))