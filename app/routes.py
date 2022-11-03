from app import db
from app.models.task import Task
from flask import abort, Blueprint, jsonify, make_response, request
# from sqlalchemy import asc
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks" )

@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    title_task_query = request.args.get("title")
    sort_task_query = request.args.get("sort")
    if sort_task_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_task_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()   
    elif title_task_query is not None:
        tasks = Task.query.filter_by(title=title_task_query)    
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    choosen_task = get_task_from_id(task_id)
    return jsonify({"task": choosen_task.to_dict()}), 200
    # return jsonify({[choosen_task.to_dict()["task"]]}), 200

@tasks_bp.route("", methods = ["POST"])
def create_one_task():
    request_body = request.get_json()
    try:
        new_task = Task(title= request_body["title"],
                        description=request_body["description"])
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201
    # return jsonify({new_task.to_dict()}), 201

@tasks_bp.route("/<task_id>", methods= ["PUT"])
def update_one_task(task_id):
    updated_task = get_task_from_id(task_id)
    request_body = request.get_json()
    
    list_keys = ["title", "description"]
    str_resp = ""
    try:
        updated_task.title = request_body["title"]
        updated_task.description = request_body["description"]
    except KeyError:
        for key in list_keys:
            if key not in request_body:
                str_resp += key + " "
        return make_response(f"Task #{task_id} missing {str_resp.strip()}", 200)
        # return make_response(jsonify({"task": f"Invalid data"}), 200)
    db.session.commit()
    return make_response(jsonify({"task": updated_task.to_dict()}), 200)

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task_to_delete = get_task_from_id(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task_to_delete.title}" successfully deleted'}), 200



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
