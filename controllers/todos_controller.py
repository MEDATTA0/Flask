from flask import json, request
from flask_restful import Resource
from sqlalchemy import inspect
from models.todos_model import Todo, Session


class TodoResources(Resource):
    def get(self, todo_id=None):
        session = Session()
        try:
            if todo_id:
                todo = session.query(Todo).filter(Todo.id == todo_id).first()
                print(todo)
                if todo != None:
                    # To serialize SQLAlchemy object to JSON with to_dict() from sqlalchemy-serializer
                    todo = todo.to_dict()
                    return {
                        "status": "success",
                        "message": "Todo found",
                        "data": todo,
                    }, 200
                else:
                    return {
                        "status": "failure",
                        "message": "Todo not found",
                        "id": todo_id,
                    }, 404
            else:
                todos = session.query(Todo).all()
                if todos:
                    return {
                        "status": "success",
                        "message": "Todos found",
                        "data": [todo.to_dict() for todo in todos],
                    }, 200
                else:
                    return {"status": "failure", "message": "No todos found"}, 404
        finally:
            session.close()

    def post(self):
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        # else:
        #     data = request.get_data(as_text=True)

        allowed_fields = ["title", "todo_description", "is_completed"]
        not_allowed_fields = [key for key in data if key not in allowed_fields]

        if not_allowed_fields:
            return {
                "status": "failure",
                "message": "Not allowed fields",
                "fields": not_allowed_fields,
            }, 400

        if "is_completed" in data:
            if data["is_completed"] in ["True", "true"]:
                data["is_completed"] = True

            elif data["is_completed"] in ["False", "false"]:
                data["is_completed"] = False
            else:
                return {
                    "status": "failure",
                    "message": "is_completed must be a boolean",
                }, 400

        session = Session()
        new_todo = Todo(**data)
        print(new_todo)
        session.add(new_todo)
        session.commit()
        session.close()

        return {
            "status": "success",
            "message": "Todo created",
            "data": data,
        }, 201

    def patch(self, todo_id):
        session = Session()
        try:
            if request.json:
                data = request.get_json()
            else:
                data = request.form
            # else:
            #     data = request.get_data(as_text=True)
            # data = json.loads(data)
            allowed_fields = ["title", "todo_description", "is_completed"]
            not_allowed_fields = [key for key in data if key not in allowed_fields]

            if not_allowed_fields:
                return {
                    "status": "failure",
                    "message": "Not allowed fields",
                    "fields": not_allowed_fields,
                }, 400

            if "is_completed" in data:
                if data["is_completed"] in ["True", "true"]:
                    data["is_completed"] = True

                elif data["is_completed"] in ["False", "false"]:
                    data["is_completed"] = False
                else:
                    return {
                        "status": "failure",
                        "message": "is_completed must be a boolean",
                    }, 400

            row_count = session.query(Todo).filter(Todo.id == todo_id).update(data)
            session.commit()
            if row_count:
                todo = session.query(Todo).filter(Todo.id == todo_id).first()
                # to serialize from SQLAlchemy object to JSON
                todo = todo.to_dict()
                return {
                    "status": "success",
                    "message": "Todo updated",
                    "data": todo,
                }, 200
            else:
                return {
                    "status": "failure",
                    "message": "Todo not found",
                    "id": todo_id,
                }, 404
        finally:
            session.close()

    def delete(self, todo_id):
        session = Session()
        try:
            row_count = session.query(Todo).filter(Todo.id == todo_id).delete()
            session.commit()
            if row_count:
                return {
                    "status": "success",
                    "message": "Todo deleted successfully",
                    "id": todo_id,
                }, 200
            else:
                return {
                    "status": "failure",
                    "message": "Todo not found",
                    "id": todo_id,
                }, 404
        finally:
            session.close()
