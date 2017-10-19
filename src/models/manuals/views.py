from flask import Blueprint, send_file, render_template, request, url_for, redirect

from src.models.manuals.manual import Manual

manual_blueprint = Blueprint('manuals', __name__)


@manual_blueprint.route('/')
def show_manuals():
    manuals = Manual.get_all()
    return render_template("/manuals/show_all.jinja2", manuals=manuals)


@manual_blueprint.route('/add/', methods=['POST', 'GET'])
def create_manual():
    if request.method == 'POST':
        file_name = request.form['file_name']
        path = request.form['path']
        description = request.form['description']
        if Manual(file_name, path, description).save_to_db():
                return redirect(url_for(".show_manuals"))
    return render_template("/manuals/create_manual.jinja2")


@manual_blueprint.route('/dowload/<string:file_name>')
def download(file_name):
    file = Manual.get_manual_by_name(file_name)
    try:
        return send_file(file.path, attachment_filename=file.file_name)
    except Exception as e:
        return str(e)


@manual_blueprint.route('/delete/<string:file_name>')
def delete(file_name):
    try:
        Manual.delete_manual(file_name)
        return redirect(url_for(".show_manuals"))
    except Exception as e:
        return str(e)
