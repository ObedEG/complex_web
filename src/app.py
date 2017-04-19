from flask import Flask, render_template

from src.common.database import Database
from src.models.manuals.views import manual_blueprint
from src.models.racks.views import rack_blueprint
from src.models.tasks.views import task_blueprint
from src.models.users.views import user_blueprint
from src.models.failures.views import failure_blueprint
from src.models.fixes.views import fix_blueprint

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "123"

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(rack_blueprint, url_prefix="/racks")
app.register_blueprint(task_blueprint, url_prefix="/tasks")
app.register_blueprint(manual_blueprint, url_prefix="/manuals")
app.register_blueprint(failure_blueprint, url_prefix="/failures")
app.register_blueprint(fix_blueprint, url_prefix="/fixes")


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template("home.jinja2")
