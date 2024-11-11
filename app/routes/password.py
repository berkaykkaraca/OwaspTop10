from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from app import app, mysql
from app.forms import PasswordForm, ResetPasswordForm, ChangePasswordForm
from app.decorators import login_required
from passlib.hash import sha256_crypt
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
global tempcode
password_bp = Blueprint("password",__name__)
@password_bp.route("/forgotpassword", methods=["GET", "POST"])
def forgotPassword():
    form = PasswordForm(request.form)
    if request.method == "POST":
        cur = mysql.connection.cursor()
        s = "SELECT email FROM student WHERE email =%s"
        email1 = form.email.data
        result = cur.execute(s, (email1,))
        if result > 0:
            email = cur.fetchone()
            sendMail(email1)
            return redirect(url_for("password.resetPassword", email=email1))
        else:
            flash("Wrong Email..", "danger")
            return redirect(url_for("password.forgotPassword"))
    else:
        return render_template("/student/forgotpassword.html", form=form)

@password_bp.route("/resetpassword/<email>", methods=["GET", "POST"])
def resetPassword(email):
    global tempcode
    form = ResetPasswordForm(request.form)
    if request.method == "POST":
        submitted_code = form.code.data
        code = tempcode
        if str(submitted_code) == str(code):
            tempcode = 0
            session["temp"]=email
            return redirect(url_for("password.changePassword", email=email))
        else:
            flash("Kod yanlış", "danger")
            return redirect(url_for("password.resetPassword", email=email))
    else:
        return render_template("/student/resetpassword.html", email=email, form=form)

@password_bp.route("/changepassword/<email>", methods=["GET", "POST"])
def changePassword(email):
    form = ChangePasswordForm(request.form)
    if session["temp"]==email:
        if request.method == "POST" and form.validate():
            cur = mysql.connection.cursor()
            password = sha256_crypt.encrypt(form.password.data)
            s = "UPDATE student SET password = %s WHERE email=%s"
            result = cur.execute(s, (password, email))
            mysql.connection.commit()
            flash("Your password successfully changed")
            session["temp"]=None
            return redirect(url_for("password.studentLogin"))
        else:
            return render_template("/student/changepassword.html", form=form)
    else:
        flash("Buna yetkiniz yok!", "danger")
        return redirect(url_for("password.studentLogin"))

@password_bp.route("/forgotpasswordteacher", methods=["GET", "POST"])
def forgotPasswordTeacher():
    form = PasswordForm(request.form)
    if request.method == "POST":
        cur = mysql.connection.cursor()
        s = "SELECT email FROM student WHERE email =%s"
        email1 = form.email.data
        result = cur.execute(s, (email1,))
        if result > 0:
            email = cur.fetchone()
            sendMail(email1)
            return redirect(url_for("password.resetPasswordTeacher", email=email1))
        else:
            flash("Wrong Email..", "danger")
            return redirect(url_for("password.forgotPasswordTeacher"))
    else:
        return render_template("/student/forgotpassword.html", form=form)

@password_bp.route("/resetpasswordteacher/<email>", methods=["GET", "POST"])
def resetPasswordTeacher(email):
    global tempcode
    form = ResetPasswordForm(request.form)
    if request.method == "POST":
        submitted_code = form.code.data
        code = tempcode
        if str(submitted_code) == str(code):
            tempcode = 0
            session["temp"]=email
            return redirect(url_for("password.changePasswordTeacher", email=email))
        else:
            flash("Kod yanlış", "danger")
            return redirect(url_for("password.resetPasswordTeacher", email=email))
    else:
        return render_template("/student/resetpassword.html", email=email, form=form)

@password_bp.route("/changepasswordteacher/<email>", methods=["GET", "POST"])
def changePasswordTeacher(email):
    form = ChangePasswordForm(request.form)
    if session["temp"]==email:
        if request.method == "POST" and form.validate():
            cur = mysql.connection.cursor()
            password = sha256_crypt.encrypt(form.password.data)
            s = "UPDATE teacher SET password = %s WHERE email=%s"
            result = cur.execute(s, (password, email))
            mysql.connection.commit()
            flash("Your password successfully changed")
            return redirect(url_for("teacher.teacherLogin"))
        else:
            return render_template("/student/changepassword.html", form=form)
    else:
        flash("Buna yetkiniz yok!", "danger")
        return redirect(url_for("student.studentLogin"))

def sendMail(email):
    global tempcode
    message = MIMEMultipart()
    code = random.randint(100000, 999999)
    tempcode = code
    rand = str(code)
    message["From"] = "berkay.karaca@tedu.edu.tr"
    message["To"] = email
    message["Subject"] = " Mail Gönderme"

    yazi = rand

    g = MIMEText(yazi, "plain")
    message.attach(g)
    try:
        mail = smtplib.SMTP('smtp.outlook.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login("berkay.karaca@tedu.edu.tr", "13Mart2012.")
        mail.sendmail(message["From"], message["To"], message.as_string())
        print("Mail gönderildi..")
        mail.quit()
    except Exception:
        sys.stderr.write("Sorun oluştu")
        sys.stderr.flush()
