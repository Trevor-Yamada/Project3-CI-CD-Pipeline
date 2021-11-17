
from enum import unique
from os import name
from flask import Flask,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at= db.Column(db.DateTime, nullable=False,default=datetime.now)
    priority = db.Column(db.String(80),nullable = False, default = 'Low')
    completed = db.Column(db.Boolean,default = False,nullable = False)
    def __repr__(self):
    	return f'Todo : {self.name}'


@app.route("/", methods = ['POST', 'GET'])
def home():

    if request.method == "POST":
        name = request.form['name']
        priority = request.form['priority']
        new_task = Task(name=name,priority = priority)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    else:
        tasks = Task.query.order_by(Task.created_at).all()
        return render_template("home.html", tasks = tasks,time = datetime.now)

@app.route('/delete/<int:id>')
def delete(id):
   task = Task.query.get_or_404(id)
   try:
       db.session.delete(task)
       db.session.commit()
       return redirect('/')
   except Exception:
       return "There was a problem deleting data."

@app.route('/complete/<int:id>')
def complete(id):
    task = Task.query.get_or_404(id)
    print(id)
    print(task.completed)
    if task.completed == False:
        try:
            task.completed = True
            print(task.completed)
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'could not add'
    else:
        try:
            task.completed = False
            print(task.completed)
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'could not add'
    #tasks = Task.query.filter(Task.completed==True).all()
    #print(tasks)
    
    #return render_template("home.html", completedTasks = tasks)


if __name__ == "__main__":
    app.run(debug=True)
