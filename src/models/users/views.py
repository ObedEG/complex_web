from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for(".user_in"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("/users/login.jinja2")


@user_blueprint.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        employee_num = request.form['employee_num']
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(name, last_name, employee_num, email, password):
                session['email'] = email
                return redirect(url_for(".user_in"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("/users/register.jinja2")


@user_blueprint.route('/in')
def user_in():
    return redirect(url_for('home'))


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))