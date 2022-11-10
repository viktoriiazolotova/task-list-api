from flask import abort, make_response

def get_model_from_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        return abort(make_response({"msg":f'Invalid data type: {model_id}'}, 400))

    choosen_model = cls.query.get(model_id)

    if choosen_model is None:
        return abort(make_response({"msg": f"Can not find {cls.__name__.lower()} id {model_id}"}, 404
 ))
    return choosen_model
