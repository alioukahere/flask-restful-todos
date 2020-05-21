from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@localhost:3306/<db_name>'

db = SQLAlchemy(app)

api = Api(app)

class Todo(db.Model):
    """docstring for Todo"""
    __tablename__ = 'todos' # The table name in the database
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255))
    is_done = db.Column(db.Boolean)

    def __init__(self, task, is_done=False):
        self.task = task
        self.is_done = is_done

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class TodoSchema(ModelSchema):
    """docstring for TodoSchema"""
    class Meta(ModelSchema.Meta):
        """docstring for Meta"""
        model = Todo
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    task = fields.String(required=True)
    is_done = fields.Boolean(reqparse=True)

class TodoCollection(Resource):
    """docstring for TodoCollection"""
    def get(self):
        todos = Todo.query.all() # select * from todos
        schema = TodoSchema
        data = schema(many=True).dump(todos)
        return data

    def post(self):
        data = request.get_json()
        schema = TodoSchema()
        todo = schema.load(data)
        result = schema.dump(todo.create())

        return result

class TodoItem(Resource):
    """docstring for TodoItem"""
    def get(self, todo_id):
        todo = Todo.query.get(todo_id) # select * from todos where id = todo_id

        if todo:
            schema = TodoSchema()
            result = schema.dump(todo)

            return result
        else:
            return {
                'message': 'La ressoure {} n\'existe pas.'.format(todo_id)
            }

    def put(self, todo_id):
        data = request.get_json()
        todo = Todo.query.get(todo_id)

        if todo:
            for key, value in data.items():
                setattr(todo, key, value)

            db.session.add(todo)
            db.session.commit()
            schema = TodoSchema()
            result = schema.dump(todo)

            return result
        else:
            return {
                'message': 'La ressoure {} n\'existe pas.'.format(todo_id)
            }

    def delete(self, todo_id):
        todo = Todo.query.get(todo_id)

        if todo:
            db.session.delete(todo)
            db.session.commit()

            return TodoSchema().dump(todo)
        else:
            return {
                'message': 'La ressoure {} n\'existe pas.'.format(todo_id)
            }

api.add_resource(TodoCollection, '/todos/')
api.add_resource(TodoItem, '/todos/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
