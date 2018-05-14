from flask import Blueprint, request, redirect, render_template, url_for, flash, send_file
from src.common.webtools.xcat.unit import Unit
from src.common.webtools.xcat.xcat import Xcat
from src.common.webtools.webtools_utils import WebtoolsUtils

csc_blueprint = Blueprint('csc', __name__)


@csc_blueprint.route('/main')
def main_menu():
    return render_template('csc/main_module.jinja2')


@csc_blueprint.route('/truven')
def truven_menu():
    return render_template('csc/truven_menu.jinja2')
