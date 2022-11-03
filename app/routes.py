from app import db
from app.models.task import Task
from flask import abort, Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks" )

@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    choosen_task = get_task_from_id(task_id)
    return jsonify({"task": choosen_task.to_dict()}), 200
    

@tasks_bp.route("", methods = ["POST"])
def create_one_task():
    request_body = request.get_json()
    new_task = Task(title= request_body["title"],
                    description=request_body["description"])
    db.session.add(new_task)
    db.session.commit()

    # return make_response(jsonify(f"Task {new_task.title} successuly created with id {new_task.task_id}.")), 201
    return jsonify({"task": new_task.to_dict()}), 201

def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"msg":f'Invalid data type: {task_id}'}, 400))

    choosen_task = Task.query.get(task_id)

    if choosen_task is None:
        return abort(make_response({"msg": f"Can not find task id {task_id}"}, 404
 ))
    return choosen_task
