
from flask import Flask, jsonify, request
import pandas as pd
import uuid
import io

app = Flask(__name__)

@app.route('/')
def hello_world():
   #return jsonify({'tasks': tasks})
    return 'Hello, World3!'

dataStore = pd.DataFrame(columns=['Date', 'Type', 'Amount($)', 'Memo'])
headers = ['Date', 'Type', 'Amount($)', 'Memo']

@app.route('/report', methods=['GET'])
def get_tasks():
    return dataStore.to_json(orient='records')

@app.route('/transactions', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part; I need files"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        # Read the file into a pandas DataFrame
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = pd.read_csv(stream, header=None, names=headers)
        
        # Process the DataFrame (example: print the first few rows)
        #print(csv_input.head())
        global dataStore
        dataStore = pd.concat([dataStore, csv_input], ignore_index=True)
        print(dataStore)
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

# Sample DataFrame
df = pd.DataFrame({
    'Date': ['2020-07-11', '2020-09-23', '2020-04-02'],
    'Region': ['East', 'North', 'South'],
    'Type': ["Children's Clothing", "Children's Clothing", "Women's Clothing"],
    'Units': [18, 14, 17],
    'Sales': [306, 448, 425]
})

# Filter rows where Sales > 300
filtered_df = df[df['Sales'] > 300]
print(filtered_df)



