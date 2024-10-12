from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id     #Q. Where is it used? more clarity needed


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':       
        #Q. In what cases is request.method == 'POST'?
        #A. We have specified method = 'POST' for a form tag in the HTML file
        task_content = request.form['content']  
        #'content' here refers to ID of a particular html form tag, and gets the info from it
        # so basically task_content is a string here
        new_task = Todo(content=task_content) 
        #creating an object of the Todo class/model
        # you dont need to specify other model attribues other than content because 
        # since ID is primary_key, it gets automatically assigned 
        # default is assigned for date_created
        #note that this object only has one row

        try:
            db.session.add(new_task) #takes this new object to the session (session is like a staging area for database operations)
            db.session.commit()      #data in this new object gets added to the database. 
            return redirect('/')
        except:
            return 'There was an issue adding your task' #more than 200 chars? or SQL server error

    else:           #Q. In what cases in request.method == 'GET'? 
                    #A. Default. 
        tasks = Todo.query.order_by(Todo.date_created).all()
        #Q. What if I use Todo.all() here? will it be randomly ordered?
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id): #notice that you're passing id into this function
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
