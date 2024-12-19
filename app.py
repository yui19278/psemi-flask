from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    details = db.Column(db.String(100))

@app.route("/")
def index():
    tasks = Todo.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/create", methods=["POST"])
def create():
    title = request.form.get("title")
    details = request.form.get("details")
    new_task = Todo(title=title, details=details)
    
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    deltask = Todo.query.get(id)
    db.session.delete(deltask)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>", methods=["POST"])
def upgrade(id):
    updtask = Todo.query.get(id)
    updtask.title = request.form.get("title")
    updtask.details = request.form.get("details")
    db.session.commit()
    return redirect("/")

@app.route('/edit/<int:id>', methods=["GET", "POST"])
def update(id):
    edit_task = Todo.query.get(id)
    if request.method == "GET":
        return render_template("edit.html", task=edit_task)
    else:
        edit_task.title = request.form.get("title")
        edit_task.details = request.form.get("details")
        db.session.commit()
        return redirect("/")

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)

