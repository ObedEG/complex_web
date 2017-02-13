from flask import Flask, render_template
from src import config
from src.common.database import Database
from src.models.users.views import user_blueprint
from src.models.racks.views import rack_blueprint
from src.models.tasks.views import task_blueprint

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "123"

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(rack_blueprint, url_prefix="/racks")
app.register_blueprint(task_blueprint, url_prefix="/tasks")


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template("home.jinja2")
