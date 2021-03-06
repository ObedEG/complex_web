from flask import Flask, render_template

from src.common.database import Database
from src.models.manuals.views import manual_blueprint
from src.models.racks.views import rack_blueprint
from src.models.tasks.views import task_blueprint
from src.models.users.views import user_blueprint
from src.models.failures.views import failure_blueprint
from src.models.fixes.views import fix_blueprint
from src.models.frecords.views import frecord_blueprint
from src.models.webtools.views import webtool_blueprint
from src.models.csc.views import csc_blueprint
from src.models.csc.csc_truven import csc_truven_blueprint
from src.models.csc.nutanix_cigna.views import cigna_blueprint

app = Flask(__name__)
app.config.from_object('src.config')
print(app.config['UPLOAD_FOLDER'])
app.secret_key = "123"

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(rack_blueprint, url_prefix="/racks")
app.register_blueprint(task_blueprint, url_prefix="/tasks")
app.register_blueprint(manual_blueprint, url_prefix="/manuals")
app.register_blueprint(failure_blueprint, url_prefix="/failures")
app.register_blueprint(fix_blueprint, url_prefix="/fixes")
app.register_blueprint(frecord_blueprint, url_prefix="/frecords")
app.register_blueprint(webtool_blueprint, url_prefix="/TEWebtools")
app.register_blueprint(csc_blueprint, url_prefix="/csc")
app.register_blueprint(csc_truven_blueprint, url_prefix="/csc_truven")
app.register_blueprint(cigna_blueprint, url_prefix="/cigna")


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template("home.jinja2")


@app.route('/TEWebtools/')
def dcg():
    return render_template("TEWebtools/welcome.jinja2")
