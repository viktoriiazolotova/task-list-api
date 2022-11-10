from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request
from .validation import get_model_from_id

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods = ["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]
    
    return jsonify(goals_response), 200

@goals_bp.route("<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    choosen_goal = get_model_from_id(Goal, goal_id)
    
    return jsonify({"goal": choosen_goal.to_dict()}), 200

@goals_bp.route("", methods = ["POST"])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400
    
    db.session.add(new_goal)
    db.session.commit()
    
    return jsonify({"goal": new_goal.to_dict()}), 201

@goals_bp.route("/<goal_id>", methods= ["PUT"])
def update_one_goal(goal_id):
    updated_goal = get_model_from_id(Goal,goal_id)
    request_body = request.get_json()
    try:
        updated_goal.title = request_body["title"]
    except KeyError:
        return make_response(f"Goal #{goal_id} missing title.", 200)
    
    db.session.commit()
    
    return make_response(jsonify({"goal": updated_goal.to_dict()}), 200)

@goals_bp.route('/<goal_id>', methods=['DELETE'])
def delete_one_goal(goal_id):
    goal_to_delete = get_model_from_id(Goal,goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{goal_to_delete.title}" successfully deleted'}), 200

@goals_bp.route('/<goal_id>/tasks', methods = ["POST"])
def add_tasks_ids_to_goal(goal_id):
    goal = get_model_from_id(Goal, goal_id)
    request_body = request.get_json()
    given_task_ids = request_body["task_ids"]
    
    tasks_ids_list = []
    for task_id in given_task_ids:
        task = get_model_from_id(Task, task_id)
        task.goal_id = goal.goal_id
        tasks_ids_list.append(task.task_id)
   
    db.session.commit()
   
    return jsonify({"id": goal.goal_id, "task_ids": tasks_ids_list}), 200

@goals_bp.route('/<goal_id>/tasks', methods = ["GET"])
def get_all_tasks_by_goal(goal_id):
    goal = get_model_from_id(Goal, goal_id)
    tasks = goal.get_task_ids_list()
    
    return jsonify(goal.to_dict_with_tasks()), 200  
