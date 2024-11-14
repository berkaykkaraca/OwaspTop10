from wtforms import (
    Form,
    IntegerField,
    TextAreaField,
    StringField,
    PasswordField,
    validators,
)


class RegisterForm(Form):
    name = StringField(
        "Name and Surname:",
        validators=[
            validators.length(min=4, max=25),
        ],
    )
    username = StringField(
        "Username:",
        validators=[
            validators.length(min=5, max=35),
            validators.DataRequired(message="Lütfen bir kullanıcı adı belirleyin"),
        ],
    )
    email = StringField(
        "Email:",
        validators=[
            validators.Email(message="Please Enter a Valid Email."),
            validators.DataRequired(message="Lütfen bir email adresi belirleyin"),
        ],
    )

    password = PasswordField("Password:", validators=[])
    confirm = PasswordField("Confirm Password:")


class LoginForm(Form):
    username = StringField("Username:")
    password = PasswordField("Password:")


class QuizForm(Form):
    question = TextAreaField("Question:", validators=[validators.DataRequired()])
    choice1 = StringField("Choice 1:", validators=[validators.DataRequired()])
    choice2 = StringField("Choice 2:", validators=[validators.DataRequired()])
    choice3 = StringField("Choice 3:", validators=[validators.DataRequired()])
    choice4 = StringField("Choice 4:", validators=[validators.DataRequired()])
    RightAnswer = IntegerField("Right Answer:", validators=[validators.DataRequired()])


class ArticleForm(Form):
    title = StringField("Title:", validators=[validators.length(min=5, max=40)])
    url = StringField("Url:", validators=[validators.URL(), validators.Optional()])
    content = TextAreaField("Content:", validators=[validators.length(min=10)])


class QuestionForm(Form):
    title = StringField("Title:", validators=[validators.DataRequired()])
    question = TextAreaField("Question:", validators=[validators.DataRequired()])


class AnswerForm(Form):
    answer = TextAreaField(
        "",
        validators=[validators.DataRequired()],
        render_kw={"placeholder": "Enter your answer here"},
    )


class PasswordForm(Form):
    email = StringField(
        "Email:",
        validators=[
            validators.Email(message="Please Enter a Valid Email."),
            validators.DataRequired(message="Lütfen bir email adresi belirleyin"),
        ],
    )


class ResetPasswordForm(Form):
    code = StringField("Code")


class ChangePasswordForm(Form):
    password = PasswordField(
        "Password:",
        validators=[
            validators.length(min=7, max=35),
            validators.EqualTo("confirm", message="Parolanız uyuşmuyor."),
            validators.DataRequired(message="Lütfen bir şifre belirleyin."),
        ],
    )
    confirm = PasswordField("Confirm Password:")
