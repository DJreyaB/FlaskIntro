# import libraries
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#create table structure
class Todo(db.Model):
    # __tablename__ = 'todo'
    usr_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 


    def __repr__(self):
        '''
        Returns task and id when new task is created.
        '''
        return '<Task %r>' % self.id

# create an index route with post and get methods
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)


if __name__ == "__main__":
    app.run(debug=True)
