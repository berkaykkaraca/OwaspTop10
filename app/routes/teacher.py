from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from app import app, mysql
from app.forms import RegisterForm, LoginForm
from app.decorators import login_required
from passlib.hash import sha256_crypt

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route("/teacher/register", methods=["GET", "POST"])
def teacherRegister():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        try:
            cursor = mysql.connection.cursor()
            s = "INSERT INTO teacher(name,username,email,password,type) VALUES(%s,%s,%s,%s,'teacher')"
            cursor.execute(s, (name, username, email, password))
            mysql.connection.commit()
        except mysql.connection.IntegrityError as err:
            flash("This username has taken.", "danger")
            return redirect(url_for("teacher.teacherRegister"))
        cursor.close()
        flash("Başarıyla Kayıt oldunuz.", "success")
        return redirect(url_for("teacher.teacherLogin"))
    else:
        return render_template("/teacher/register.html", form=form)

@teacher_bp.route("/teacher/login", methods=["GET", "POST"])
def teacherLogin():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        cursor = mysql.connection.cursor()
        s = "SELECT * FROM teacher WHERE username=%s;"
        result = cursor.execute(s, (username,))
        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password, real_password):
                flash("Başarıyla giriş yaptınız...", "success")
                session["logged_in"] = True
                session["username"] = username
                session["type"] = "teacher"
                return redirect(url_for("main.index"))
            else:
                flash("Parolanız yanlış", "danger")
                return redirect(url_for("teacher.teacherLogin"))
        else:
            flash("Böyle bir kullanıcı bulunmuyor...", "danger")
            return redirect(url_for("teacher.teacherLogin"))
    return render_template('/teacher/login.html', form=form)
