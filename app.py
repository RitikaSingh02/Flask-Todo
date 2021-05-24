from flask import Flask, render_template, request, redirect, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
# mysql://username:password@host/dbname
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# print(db)

migrate = Migrate(app, db)
app.config['SECRET_KEY'] = os.getenv('DATABASE_URI')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800
# define the schema


@app.errorhandler(404)
def not_found(e):
    # defining function
    return render_template("404.html")


class User(db.Model):
    _tablename = 'user'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}- {self.uname}"


class Todo(db.Model):
    _tablename = 'todo'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    user = db.Column(db.String(200), db.ForeignKey('user.uname'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}- {self.desc}-{self.date_created}"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user" not in session:
        if request.method == "POST":
            uname = request.form["username"]
            password = request.form["password"]
            if User.query.filter_by(uname=uname).first() is None:
                user = User(uname=uname, password=password)
                db.session.add(user)
                db.session.commit()
                session['user'] = uname
                return redirect(url_for('home'))
            elif User.query.filter_by(uname=uname,
                                      password=password).first() is None:
                return render_template('login.html', msg="Invalid Credentials")
            else:
                session['user'] = uname
                return redirect(url_for('home'))
        return render_template('login.html')
    else:
        return redirect(url_for('home'))


@app.route('/', methods=['GET', 'POST'])
def home():
    if "user" in session:
        uname = session['user']
        if request.method == "POST":
            title = request.form["title"]
            desc = request.form["desc"]
            todo = Todo(title=title, desc=desc, user=uname)
            db.session.add(todo)
            db.session.commit()

        allqueries = Todo.query.filter_by(user=uname).all()
        return render_template('index.html', allqueries=allqueries, user=uname)
    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno, user=session['user']).first()
    if todo is None:
        return render_template("404.html")
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if 'user' in session:
        todo = Todo.query.filter_by(sno=sno, user=session['user']).first()
        if todo is None:
            return render_template("404.html")
        if request.method == "POST":
            title = request.form["title"]
            desc = request.form["desc"]
            todo.title = title
            todo.desc = desc
            db.session.add(todo)
            db.session.commit()
            return redirect("/")
        return render_template("update.html", todo=todo, user=session['user'])
    else:
        return render_template("login_alert.html")


@app.route('/search')
def search():
    if 'user' in session:
        allqueries = Todo.query.filter_by(user=session['user'])
        ans = []
        for task in allqueries:
            ans.append([task.sno, task.title, task.desc])

        return {"res": ans}
    else:
        return render_template('login_alert.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
