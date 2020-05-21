# Flask-restful todos

A simple todo API (Yes another one) made with Flask and Flask-restful

## Installation

Activate the virtual environment with:

```bash
$ source env/bin/activate
```

Then install the dependencies with ``pip``:

```bash
$ pip install -r requirements.txt
```

Set your database access in <code>__init__.py</code>

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@localhost:3306/<db_name>'
```

Replace <code><username></code> by your database user <code><password></code> by his password and <code><db_name></code> by your database name.

Open a python interpreter and create the tables:

```python
>>> from app import db
>>> db.create_all()
```

## Run the app

To run the app:

```bash
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run
```

Navigate to http://127.0.0.1:5000/todos/ and you're done.
