from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('task', type=str, required=True,
    help='Veillez renseigner le libéllé de la tache.', location='json')
parser.add_argument('is_done', type=bool, default=False, location='json')

todos = [
    {
        'todo_id': 1,
        'task': 'Suivre le cours Python sur Kaherecode',
        'is_done': False,
    },
    {
        'todo_id': 2,
        'task': 'Faire la vaisselle',
        'is_done': True,
    },
]

class Todo(object):
    """docstring for Todo"""
    def __init__(self, todo_id, task, is_done=False):
        self.todo_id = todo_id
        self.task = task
        self.is_done = is_done


class TodoCollection(Resource):
    """docstring for TodoCollection"""
    def get(self):
        return todos

    def post(self):
        data = parser.parse_args()

        todo = Todo(len(todos)+1, data['task'], data['is_done'])
        todos.append(todo.__dict__)

        return todo.__dict__


class TodoItem(Resource):
    """docstring for TodoItem"""
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('task', type=str, location='json')
        self.parser.add_argument('is_done', type=bool, location='json')

    def get(self, todo_id):
        try:
            return todos[todo_id-1]
        except IndexError as e:
            return {
                'message': 'La ressoure {} n\'existe pas.'.format(todo_id)
            }

    def put(self, todo_id):
        if todo_id <= 0 or todo_id > len(todos):
            return {
                'message': 'La ressoure {} n\'existe pas.'.format(todo_id)
            }

        todo = todos[todo_id-1]
        data = self.parser.parse_args()

        # if data['task']:
        #     todo['task'] = data['task']
        # if data['is_done']:
        #     todo['is_done'] = data['is_done']

        for key, value in data.items():
            if value:
                todo[key] = value

        todos[todo_id-1] = todo

        return todo

    def delete(self, todo_id):
        if todo_id <= 0 or todo_id > len(todos):
            return {
                'message': 'La ressoure {} n\'existe pas.'.format(todo_id)
            }

        todo = todos.pop(todo_id-1)

        return todo


api.add_resource(TodoCollection, '/todos/')
api.add_resource(TodoItem, '/todos/<int:todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
