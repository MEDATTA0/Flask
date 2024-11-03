from flask import json, jsonify, request
from flask_restful import Resource
from sqlalchemy import inspect
from models.todos_model import Todo, Session


class TodoResources(Resource):
    def get(self, todo_id=None):
        session = Session()
        try:
            if todo_id == None:
                todos = session.query(Todo).all()
                data = [todo.serialize_to_json() for todo in todos]
                if todos:
                    return (
                        {
                            "status": "success",
                            "message": "todos found",
                            "data": data,
                        },
                        200,
                    )
                else:
                    return {"status": "failure", "message": "no todos found"}, 404
            elif todo_id > 0:

                todo = session.query(Todo).filter(Todo.id == todo_id).first()
                print(todo)
                if todo != None:
                    # To serialize SQLAlchemy object to JSON with to_dict() from sqlalchemy-serializer
                    todo = todo.to_dict()
                    return {
                        "status": "success",
                        "message": "todo found",
                        "data": todo,
                    }, 200
                else:
                    return {
                        "status": "failure",
                        "message": "todo not found",
                        "id": todo_id,
                    }, 404
            else:
                return {
                    "status": "failure",
                    "message": "todo id must be strictly positive",
                    "id": todo_id,
                }, 400

        finally:
            session.close()

    def post(self, todo_id=None):
        if todo_id != None:
            return {
                "status": "failure",
                "message": "todo id is not allowed in url POST method",
            }, 400

        else:
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form
            # else:
            #     data = request.get_data(as_text=True)
            if len(data) == 0:
                return {
                    "status": "failure",
                    "message": "the body request cannot be empty",
                }, 400
            else:
                allowed_fields = ["title", "todo_description", "is_completed"]
                not_allowed_fields = [key for key in data if key not in allowed_fields]
                # if todo_id != None:
                #     not_allowed_fields.append("todo id")

                if not_allowed_fields:
                    return {
                        "status": "failure",
                        "message": "not allowed fields",
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
                    "message": "todo created",
                    "data": data,
                }, 201

    def patch(self, todo_id=None):
        if todo_id == None or todo_id <= 0:
            return {
                "status": "failure",
                "message": "todo id is required and can't be negative or null",
                "id": todo_id,
            }, 400

        else:
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
                        "message": "not allowed fields",
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
                        "message": "todo updated",
                        "data": todo,
                    }, 200
                else:
                    return {
                        "status": "failure",
                        "message": "todo not found",
                        "id": todo_id,
                    }, 404
            finally:
                session.close()

    def delete(self, todo_id=None):
        if todo_id == None or todo_id <= 0:
            return {
                "status": "failure",
                "message": "todo id can't be negative or null",
                "id": todo_id,
            }, 400

        else:
            session = Session()
            try:
                row_count = session.query(Todo).filter(Todo.id == todo_id).delete()
                session.commit()
                if row_count:
                    return {
                        "status": "success",
                        "message": "todo deleted successfully",
                        "id": todo_id,
                    }, 200
                else:
                    return {
                        "status": "failure",
                        "message": "todo not found",
                        "id": todo_id,
                    }, 404
            finally:
                session.close()
