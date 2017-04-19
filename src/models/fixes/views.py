from flask import Blueprint, send_file, render_template, request, url_for, redirect
import src.models.users.decorators as user_decorators
from src.models.failures.failure import Failure
from src.models.fixes.fix import Fix
from src.models.racks.rack import Rack
from src.models.tasks.task import Task

fix_blueprint = Blueprint('fixes', __name__)


@fix_blueprint.route('/add/<string:rack>/<string:task>/<string:failure>', methods=['GET', 'POST'])
@user_decorators.requires_login
def add_new_fix(rack, task, failure):
    #
    #  If the input is less than 20 characters, create the FIX and render the rack_tasks again
    #
    if request.method == 'POST':
        if len(request.form["text"]) < 20:
            return render_template('fixes/wrong_fix_description.jinja2', task=task, rack=rack, failure=failure)
        fix = Fix(rack=rack, failure=failure, task=task, category=Task.get_task_by_id(task).category,
                  description=request.form["text"])
        fix.save_to_db()
        failure_to_update = Failure.get_failure_by_id(failure)
        failure_to_update.add_fix(fix._id)
        #  If the fix was added successfuly, render again the rack_tasks
        rack_look_up = Rack.get_rack_by_id(rack)
        taskid_list = rack_look_up.tasks
        tasks = []
        for elem in taskid_list:
            tasks.append(Task.get_task_by_id(elem))
        return redirect(url_for('tasks.continue_test', rack=rack))
    #  This is for GET requests...to create create an aditional fix
    return render_template('fixes/add_fix.jinja2', failure=failure, rack=rack, task=task)


@fix_blueprint.route('/test/passed/<string:fix>', methods=['GET', 'POST'])
@user_decorators.requires_login
def passed(fix):
    fix_pass = Fix.get_fix_by_id(fix)
    fix_pass.passed()
    Task.get_task_by_id(fix_pass.task).finish()
    Failure.get_failure_by_id(fix_pass.failure).finish()
    rack_in_test = Rack.get_rack_by_id(fix_pass.rack)
    rack_in_test.start_rack()
    taskid_list = rack_in_test.tasks
    tasks = []  # Empty list of task Object
    # iterating the tasks list of the rack to put the next task running
    for elem in taskid_list:
        if elem == Task.get_task_by_id(fix_pass.task)._id:
            if elem != taskid_list[-1]:
                next_task = Task.get_task_by_id(taskid_list[taskid_list.index(elem)+1])
                next_task.start()  # Setting the next task in "running"
            else:
                rack_in_test.finish_rack()  # If it's last task, rack pass
        tasks.append(Task.get_task_by_id(elem))
    return redirect(url_for('tasks.continue_test', rack=fix_pass.rack))


@fix_blueprint.route('/feedback/<string:fix>', methods=['GET', 'POST'])
@user_decorators.requires_login
def feedback(fix):
    if request.method == 'POST':
        if (len(request.form["textFeedback"]) < 20) or (len(request.form["textNewTask"]) < 20):
            return render_template('fixes/wrong_feedback.jinja2', fix=fix)
        else:
            # Update feedback and create new fix
            # --- Updating feedback for current failed fix
            old_fix = Fix.get_fix_by_id(fix)
            old_fix.failed(request.form["textFeedback"])
            # --- Creating new fix, add it to failure list
            new_fix = Fix(rack=old_fix.rack, failure=old_fix.failure, task=old_fix.task,
                          category=Task.get_task_by_id(old_fix.task).category, description=request.form["textNewTask"])
            new_fix.save_to_db()
            Failure.get_failure_by_id(old_fix.failure).add_fix(new_fix._id)
            tasks = []  # Empty list of task Object
            tasksid_list = Rack.get_rack_by_id(old_fix.rack).tasks
            for elem in tasksid_list:
                tasks.append(Task.get_task_by_id(elem))
            return redirect(url_for('tasks.continue_test', rack=old_fix.rack))
    else:
        actual_fix = Fix.get_fix_by_id(fix)
        return render_template('fixes/feedback.jinja2', fix=actual_fix)


#  This is the trick to return the Failure or Fix object to the DOM (kind of special wrapper)
@fix_blueprint.context_processor
def utility_task():
        def get_failure(failure):
            return Failure.get_failure_by_id(failure)

        def get_fix(fix):
            return Fix.get_fix_by_id(fix)

        def get_rack(rack):
            print("---------Here is the rack id : {}".format(rack))
            return Rack.get_rack_by_id(rack)

        return dict(get_failure=get_failure, get_fix=get_fix, get_rack=get_rack)
