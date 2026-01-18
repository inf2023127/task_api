from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
DATA_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            return jsonify(t)
    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    tasks = load_tasks()

    new_id = len(tasks) + 1
    task = {
        "id": new_id,
        "username": data["username"],
        "title": data["title"],
        "description": data["description"],
        "deadline": data["deadline"]
    }

    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    app.run(debug=True)

