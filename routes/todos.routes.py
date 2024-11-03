from flask import Blueprint

todo_bp = Blueprint('todos', __name__)


todo_bp.route("/", ["POST"])

todo_bp.route("/<todoId>", ["GET"])

todo_bp.route("/allTodos", ["GET"])

todo_bp.route("/", ["GET"])


