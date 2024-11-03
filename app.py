from flask import Flask
from flask_restful import Api
from controllers.todos_controller import TodoResources

app = Flask(__name__)
api = Api(app)

# with strict_slashes=False,flask recognize /todos and /todos/ as the same
api.add_resource(TodoResources, "/todos", "/todos/<int:todo_id>", strict_slashes=False)


@app.route("/")
def hello_world():
    return "<p>Hello World !</p>"


if __name__ == "__main__":
    app.run(debug=True)
