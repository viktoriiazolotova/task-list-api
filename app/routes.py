from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks" )

@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200
