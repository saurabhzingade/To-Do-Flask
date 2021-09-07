from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:root@localhost/zincsyblog"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(200),nullable=False)
    date = db.Column(db.DateTime,default=datetime.now())

    def __repr__(self) ->str:
        return f"{self.sno} - {self.title}"


@app.route("/",methods=["POST","GET"])
def hello_world():
    #todo=Todo(title="Second Todo",desc="Start learning programming")
    if(request.method=="POST"):
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    # todo=Todo(title="Second Todo",desc="Start learning programming")
    '''db.session.add(todo)
    db.session.commit()'''
    allTodo = Todo.query.all()
    return render_template("index.html",allTodo=allTodo)

''''@app.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "<p>Hello, This is products page!</p>"'''

@app.route("/delete/<int:sno>")
def delete(sno):
    allTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:sno>",methods=["POST","GET"])
def edit(sno):

    if request.method =="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    allTodo = Todo.query.filter_by(sno=sno).first()
    return render_template("edit.html",allTodo=allTodo)

if __name__=="__main__":
    app.run(debug=True)