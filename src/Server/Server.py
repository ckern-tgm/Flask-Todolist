from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import json

app = Flask(__name__)
api = Api(app)
CORS(app)


def save():
    global TODOS
    with open('db.json','w') as file:
        file.write(json.dumps(TODOS))


def read():
    with open('db.json','r') as file:
        global TODOS
        TODOS = json.loads(file.read())


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        read()
        abort_if_todo_doesnt_exist(todo_id)
        save()
        return TODOS[todo_id], 201

    def delete(self, todo_id):
        read()
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        save()
        return '', 204

    def put(self, todo_id):
        read()
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        save()
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        read()
        return TODOS

    def post(self):
        read()
        args = parser.parse_args()
        if(args['task'] == None):
            return "enter description"
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        save()
        return "Todo added", 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)