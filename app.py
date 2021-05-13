from flask import Flask, render_template, request, redirect
from flask.wrappers import Request
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
f = open("db.txt", "r")
# mysql://username:password@host/dbname
app.config['SQLALCHEMY_DATABASE_URI'] = f.read()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
print(db)

# define the schema


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}- {self.desc}-{self.date_created}"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allqueries = Todo.query.all()
    return render_template('index.html', allqueries=allqueries)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)


@app.route('/search')
def search():
    allqueries = Todo.query.all()
    ans = []
    for task in allqueries:
        ans.append([task.sno, task.title, task.desc])

    return {"res": ans}


if __name__ == "__main__":
    app.run(debug=True, port=8080)
