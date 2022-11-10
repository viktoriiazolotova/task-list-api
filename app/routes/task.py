from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request
from datetime import datetime
from ..slack_bot import send_message_to_slack 
from .validation import get_model_from_id

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
      
    tasks_response = [task.to_dict() for task in tasks]
   
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    choosen_task = get_model_from_id(Task,task_id)
    return jsonify({"task": choosen_task.to_dict()}), 200
    
@tasks_bp.route("", methods = ["POST"])
def create_one_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201
   
@tasks_bp.route("/<task_id>", methods= ["PUT"])
def update_one_task(task_id):
    updated_task = get_model_from_id(Task,task_id)
    request_body = request.get_json()
    
    list_keys = ["title", "description"]
    str_response = ""
    try:
        updated_task.title = request_body["title"]
        updated_task.description = request_body["description"]
    except KeyError:
        for key in list_keys:
            if key not in request_body:
                str_response += key + ", "
        return make_response(f"Task #{task_id} missing {str_response.strip()[:-1]}.", 200)
        
    db.session.commit()
    return make_response(jsonify({"task": updated_task.to_dict()}), 200)

@tasks_bp.route("/<task_id>/mark_complete", methods= ["PATCH"])
def mark_complete_one_task(task_id):
    completed_task = get_model_from_id(Task,task_id)
    completed_task.completed_at = datetime.now()
    text_to_slack = f"Someone just completed the task {completed_task.title}."
    send_message_to_slack(text_to_slack)
    
    db.session.commit()
    
    return make_response(jsonify({"task": completed_task.to_dict()}), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods= ["PATCH"])
def mark_incomplete_one_task(task_id):
    completed_task = get_model_from_id(Task,task_id)
    completed_task.completed_at = None
    
    db.session.commit()
    
    return make_response(jsonify({"task": completed_task.to_dict()}), 200)    
    
@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task_to_delete = get_model_from_id(Task,task_id)

    db.session.delete(task_to_delete)
    db.session.commit()
    
    return jsonify({"details": f'Task {task_id} "{task_to_delete.title}" successfully deleted'}), 200





