from app import db

class Goal(db.Model):
    '''
    A class to represent a goal with attributes: goal_id, title and list of tasks.
    '''
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', back_populates = "goal", lazy = True)
    
    def to_dict(self):
        goal_dict = {"id": self.goal_id,
                "title": self.title}
        return goal_dict

    def to_dict_with_tasks(self):
        goal_dict = {"id": self.goal_id,
                "title": self.title,
                "tasks": self.get_task_ids_list()}
        return goal_dict

    def get_task_ids_list(self):
        return [task.to_dict() for task in self.tasks]

    @classmethod
    def from_dict(cls, goal_dict):
        return cls(title=goal_dict["title"])