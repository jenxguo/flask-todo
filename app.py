from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite Database concept
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# App Route Decorator Concept
@app.route('/')
def index():
    todo_list = Todo.query.all()
    # Reusable Components/Templates Concept
    return render_template('base.html', todo_list=todo_list)

# App Route Decorator Concept
@app.route("/add", methods=["POST"])
def add():
    with app.app_context():
        # HTTP Request Concept
        title = request.form.get("title")
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        # Redirect Concept
        return redirect(url_for("index"))

# App Route Decorator Concept
@app.route("/update/<int:todo_id>")
def update(todo_id):
    with app.app_context():
        todo = Todo.query.filter_by(id=todo_id).first()
        todo.complete = not todo.complete
        db.session.commit()
        # Redirect Concept
        return redirect(url_for("index"))

# App Route Decorator Concept
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    with app.app_context():
        todo = Todo.query.filter_by(id=todo_id).first()
        db.session.delete(todo)
        db.session.commit()
        # Redirect Concept
        return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=8000)