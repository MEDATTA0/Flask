import pytest
import requests

BASE_URL = "http://localhost:5000"


class TestGETTodos:
    def test_get_todos(self):
        response = requests.get(f"{BASE_URL}/todos")
        assert response.status_code == 200
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "todos found"
        assert "data" in response_json
        # assert "status" in response.json()  # == "success"
        # assert "message" in response.json()  # == "todos found"
        # assert "data" in response.json()

    def test_get_todo(self):
        response = requests.get(f"{BASE_URL}/todos/20")
        assert response.status_code == 200
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "todo found"
        assert "data" in response_json

    def test_get_not_found(self):
        response = requests.get(f"{BASE_URL}/todos/200")
        assert response.status_code == 404
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "todo not found"
        assert "id" in response_json

    def test_get_todo_error_1(self):
        response = requests.get(f"{BASE_URL}/todos/0")
        assert response.status_code == 400
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "todo id must be strictly positive"
        assert "id" in response_json


class TestPOSTTodos:
    def test_post_error_todo_id_not_allowed(self):
        response = requests.post(f"{BASE_URL}/todos/1", json={})
        assert response.status_code == 400
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "todo id is not allowed in url POST method"

    def test_post_error_empty_field(self):
        response = requests.post(f"{BASE_URL}/todos", json={})
        assert response.status_code == 400
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "the body request cannot be empty"

    def test_post_error_not_allowed_fields(self):
        new_todo = {
            "title": "Demain ce sera the gym",
            "lajdflksa": "lajfklsdjf",
            "yeah": "yafor",
        }
        response = requests.post(f"{BASE_URL}/todos", json=new_todo)
        assert response.status_code == 400
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "not allowed fields"
        assert "fields" in response_json

    def test_post_error_is_completed_to_be_boolean(self):
        new_todo = {"title": "Tomorrow is the gym", "is_completed": "lakjdfd"}
        response = requests.post(f"{BASE_URL}/todos", json=new_todo)
        assert response.status_code == 400
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "is_completed must be a boolean"

    def test_post_success_1(self):
        new_todo = {"title": "Demain commence the gym"}
        response = requests.post(f"{BASE_URL}/todos", json=new_todo)
        assert response.status_code == 201
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "todo created"
        assert "data" in response_json

    def test_post_success_2(self):
        new_todo = {
            "title": "Tomorrow starts the gym",
            "todo_description": "the challenge is to do 5h a day in javascript learning",
            "is_completed": "false",
        }
        response = requests.post(f"{BASE_URL}/todos", json=new_todo)
        assert response.status_code == 201
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "todo created"
        assert "data" in response_json


class TestPatchTodo:
    def test_patch_error_todo_id_is_null(self):
        response = requests.patch(f"{BASE_URL}/todos", json={})
        assert response.status_code == 400
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert (
            response_json["message"]
            == "todo id is required and can't be negative or null"
        )

    def test_patch_error_todo_id_is_zero(self):
        response = requests.patch(f"{BASE_URL}/todos/0", json={})
        assert response.status_code == 400
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert (
            response_json["message"]
            == "todo id is required and can't be negative or null"
        )

    def test_patch_error_not_allowed_fields(self):
        new_todo = {
            "title": "Demain ce sera the gym",
            "aljaoiueoiweeoiiddmc": "lajfklsdjf",
            "yoy": "yafor",
        }
        response = requests.patch(f"{BASE_URL}/todos/25", json=new_todo)
        assert response.status_code == 400
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "not allowed fields"
        assert "fields" in response_json

    def test_patch_error_is_completed_to_be_boolean(self):
        new_todo = {"is_completed": "lakjdfd"}
        response = requests.patch(f"{BASE_URL}/todos/25", json=new_todo)
        assert response.status_code == 400
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "is_completed must be a boolean"

    def test_patch_success_1(self):
        data_to_update = {"is_completed": "true"}
        response = requests.patch(f"{BASE_URL}/todos/25", json=data_to_update)
        assert response.status_code == 200
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "todo updated"
        assert "data" in response_json

    def test_patch_success_2(self):
        data_to_update = {
            "title": "se mettre à fond",
            "todo_description": "Ça ira in shaa Allah",
            "is_completed": "true",
        }
        response = requests.patch(f"{BASE_URL}/todos/27", json=data_to_update)
        assert response.status_code == 200
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "todo updated"
        assert "data" in response_json

    def test_patch_success_1(self):
        data_to_update = {"is_completed": "true"}
        response = requests.patch(f"{BASE_URL}/todos/2", json=data_to_update)
        assert response.status_code == 404
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "todo not found"
        assert "id" in response_json


class TestDeleteTodo:
    def test_delete_error_todo_id_is_null(self):
        response = requests.delete(f"{BASE_URL}/todos")
        assert response.status_code == 400
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "todo id can't be negative or null"

    def test_delete_error_todo_id_is_not_positive_1(self):
        response = requests.delete(f"{BASE_URL}/todos/0")
        assert response.status_code == 400
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "todo id can't be negative or null"

    # I don't know why, but when the id is negative, Flask responds itself with this:
    #     <!doctype html>
    # <html lang=en>
    # <title>404 Not Found</title>
    # <h1>Not Found</h1>
    # <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try
    #     again.</p>

    # def test_delete_error_todo_id_is_not_positive_2(self):
    #     response = requests.delete(f"{BASE_URL}/todos/-1")
    #     assert response.status_code == 404
    #     assert len(response.json()) > 0
    #     response_json = response.json()
    #     assert response_json["status"] == "failure"
    #     assert response_json["message"] == "todo id can't be negative or null"

    def test_delete_success(self):
        response = requests.delete(f"{BASE_URL}/todos/3")
        assert response.status_code == 200
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "todo deleted successfully"

    def test_delete_error_todo_not_found(self):
        response = requests.delete(f"{BASE_URL}/todos/2")
        assert response.status_code == 404
        assert len(response.json()) > 0
        response_json = response.json()
        assert response_json["status"] == "failure"
        assert response_json["message"] == "todo not found"
