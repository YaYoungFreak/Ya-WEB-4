from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import EmailField


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobsForm(FlaskForm):
    job = TextAreaField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('Id капитана', validators=[DataRequired()])
    work_size = IntegerField('Объём работы в часах', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    is_finished = BooleanField('Завершена?')
    submit = SubmitField('Применить')
