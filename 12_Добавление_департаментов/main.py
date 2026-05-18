from flask import Flask, render_template, redirect, request, abort
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.department import Department
from forms import RegisterForm, LoginForm, JobsForm, DepartmentForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/')
def jobs_list():
    db_session.global_init("db/mars_explorer.db")
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('jobs.html', title="Журнал работ", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_session.global_init("db/mars_explorer.db")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   email_message="Такой пользователь уже есть")
        user = User(email=form.email.data,
                    name=form.name.data,
                    surname=form.surname.data,
                    age=form.age.data,
                    position=form.position.data,
                    speciality=form.speciality.data,
                    address=form.address.data
                    )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/register')
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = form.team_leader.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs_add.html', title='Добавление работы', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.user == current_user) | (current_user.id == 1)
                                          ).first()
        if jobs:
            form.job.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.user == current_user) | (current_user.id == 1)
                                          ).first()
        if jobs:
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs_add.html',
                           title='Редактирование работы',
                           form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      (Jobs.user == current_user) | (current_user.id == 1)
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def departments_list():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template('departments.html',
                           title='List of Departments',
                           departments=departments)


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('department_add.html',
                           title='Добавление департамента',
                           form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(
            Department.id == id,
            (Department.chief == current_user.id) | (
                current_user.id == 1)
        ).first()
        if department:
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(
            Department.id == id,
            (Department.chief == current_user.id) | (
                current_user.id == 1)
        ).first()
        if department:
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('department_add.html',
                           title='Редактирование департамента',
                           form=form)


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departments_delete(id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == id,
                                                  (Department.chief == current_user.id) | (current_user.id == 1)
                                                  ).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    app.run()
