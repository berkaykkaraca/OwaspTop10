from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from app import app, mysql
from app.forms import RegisterForm, LoginForm
from app.decorators import login_required

student_bp = Blueprint('student', __name__)

@student_bp.route("/student/register", methods=["GET", "POST"])
def studentRegister():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        #password = sha256_crypt.encrypt(form.password.data)
        cursor = mysql.connection.cursor()
        try:
            s = "INSERT INTO student(name,username,email,password,type) VALUES(%s,%s,%s,%s,'student')"
            cursor.execute(s, (name, username, email, password))
            mysql.connection.commit()
        except mysql.connection.IntegrityError as err:
            flash("This username has taken.", "danger")
            return redirect(url_for("student.studentRegister"))
        cursor.close()
        flash("Başarıyla Kayıt oldunuz.", "success")
        return redirect(url_for("student.studentLogin"))
    else:
        return render_template("/student/register.html", form=form)

@student_bp.route("/student/login", methods=["GET", "POST"])
def studentLogin():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        cursor = mysql.connection.cursor()
        s = f"SELECT * FROM student WHERE username='{username}' AND password='{password}';"
        #s= "SELECT * FROM student WHERE username='%s' AND password='%s';"
        #result = cursor.execute(s,(username,password))
        result = cursor.execute(s)
        if result > 0:
            data = cursor.fetchone()
            session["logged_in"] = True
            session["username"] = username
            session["type"] = "student"
            return redirect(url_for("main.index"))
        else:
            flash("Böyle bir kullanıcı bulunmuyor...", "danger")
            return redirect(url_for("student.studentLogin"))
    return render_template('/student/login.html', form=form)
