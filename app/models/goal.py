from app import db



class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', back_populates = "goal", lazy = True)
    
    # def to_dict(self):
    #     return {"id": self.goal_id,
    #             "title": self.title}

    def to_dict(self):
        goal_dict = {"id": self.goal_id,
                "title": self.title}
        if self.tasks :
            goal_dict["tasks"] = self.get_task_ids_list()
        # elif len(self.tasks) == 0:
        #      goal_dict["tasks"] = []
        return goal_dict

    def get_task_ids_list(self):
        tasks_ids_list = []
        for task in self.tasks:
            tasks_ids_list.append(task.to_dict())
        return tasks_ids_list

    @classmethod
    def from_dict(cls, goal_dict):
        return cls(title=goal_dict["title"])