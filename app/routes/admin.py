from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from app import app, mysql
from app.decorators import login_required, admin_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/users")
def admin():
    cursor = mysql.connection.cursor()
    s2 = "SELECT * FROM teacher WHERE username != 'admin'"
    result2 = cursor.execute(s2)
    teachers = cursor.fetchall()
    s = "SELECT * FROM student"
    result = cursor.execute(s)
    students = cursor.fetchall()
    users = teachers + students
    return render_template("/admin/admin.html", students=students, teachers=teachers)


@admin_bp.route("/admin/delete/teacher/<string:username>")
def deleteTeacher(username):
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM teacher WHERE username = %s"
    result = cursor.execute(sql, (username,))
    if result > 0:
        query = "DELETE FROM teacher WHERE username=%s"
        r2 = cursor.execute(query, (username,))
        s = "SELECT * FROM articles WHERE author=%s"
        r1 = cursor.execute(s, (username,))
        if r1 > 0:
            query1 = "DELETE FROM articles WHERE author=%s"
            cursor.execute(query1, (username,))
            mysql.connection.commit()
            flash("Successfully Deleted Teacher", "success")
            return redirect(url_for("admin.admin"))
        mysql.connection.commit()
        flash("Teacher object has been deleted.", "success")
        return redirect(url_for("admin.admin"))
    else:
        return redirect(url_for("admin.admin"))


@admin_bp.route("/admin/delete/student/<string:username>")
def deleteStudent(username):
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM student WHERE username = %s"
    result = cursor.execute(sql, (username,))
    if result > 0:
        query = "DELETE FROM student WHERE username=%s"
        r2 = cursor.execute(query, (username,))
        s = "SELECT * FROM articles WHERE author=%s"
        r1 = cursor.execute(s, (username,))
        if r1 > 0:
            query1 = "DELETE FROM articles WHERE author=%s"
            cursor.execute(query1, (username,))
            mysql.connection.commit()
            flash("Successfully Deleted Student", "success")
            return redirect(url_for("admin.admin"))
        mysql.connection.commit()
        flash("Student object has been deleted.", "success")
        return redirect(url_for("admin.admin"))
    else:
        return redirect(url_for("admin.admin"))
