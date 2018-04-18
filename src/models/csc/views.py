from flask import Blueprint, request, redirect, render_template

csc_blueprint = Blueprint('csc', __name__)


@csc_blueprint.route('/main')
def main_menu():
    return render_template('csc/main_module.jinja2')


@csc_blueprint.route('/trueven')
def trueven_menu():
    return render_template('csc/trueven_menu.jinja2')

@csc_blueprint.route('/trueven/add_unit', methods=['POST', 'GET'])
def trueven_addunit():
    if request.method == 'POST':
        # unit = MTSN(request.form['serial'])
        return render_template('csc/trueven_addunit.jinja2', server='10.34.70.220')
    return render_template('csc/trueven_addunit.jinja2')