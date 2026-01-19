from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# Route 1: GET (view all) and POST (create new)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Support for both Form data and JSON data
        if request.is_json:
            data = request.get_json()
            task_content = data.get('content')
        else:
            task_content = request.form.get('content')

        if task_content:
            new_task = Task(content=task_content)
            db.session.add(new_task)
            db.session.commit()
            
            # Return JSON response if requested, else redirect
            if request.is_json:
                return jsonify({"message": "Task created", "id": new_task.id, "content": new_task.content}), 201
        
        return redirect(url_for('index'))
    
    tasks = Task.query.all()
    
    # Return JSON if requested via headers
    if request.headers.get('Accept') == 'application/json':
        return jsonify([{"id": t.id, "content": t.content} for t in tasks])
        
    return render_template('index.html', tasks=tasks)

# Route 2: POST only (delete a task)
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    
    if request.is_json:
        return jsonify({"message": "Task deleted", "id": id})
        
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)