
from flask import Flask, jsonify, request
import uuid


tasks = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruits',
        'completed': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Learn Python',
        'description': 'Learn how to create a web service with Python',
        'completed': True
    }
]


app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({'tasks': tasks})
    #return 'Hello, World3!'




@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        # Read the file into a pandas DataFrame
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = pd.read_csv(stream)
        
        # Process the DataFrame (example: print the first few rows)
        print(csv_input.head())
        
        return jsonify({"message": "File successfully processed"}), 200

#def create_task():
#    new_task = {
#        'id': uuid.uuid4().hex,
#        'title': request.json['title'],
#       'description': 'xyz' , #request.json['description'],
#       'completed': 'yes' #request.json.get('completed', False)
#    }
#    tasks.append(new_task)
#    return jsonify({'task': new_task})

@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error': 'Task not found'})
    return jsonify({'task': task[0]})

@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error': 'Task not found'})
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['completed'] = request.json.get('completed', task[0]['completed'])
    return jsonify({'task': task[0]})

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error': 'Task not found'})
    tasks.remove(task[0])
    return jsonify({'result': 'Task deleted'})  


if __name__ == '__main__':
    app.run(host="127.0.0.6", port=5005, debug=True)



# c:\Windows\System32\curl -X GET http://127.0.0.5:5005/tasks
# c:\Windows\System32\curl -X POST http://127.0.0.5:5005/tasks -H "Content-Type:application/json" --data '{\"title\" : \"t6\"}'

