from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
app.json.sort_keys = False

# --- BASES DE DATOS TEMPORALES (EN MEMORIA) ---
tasks = [] 

users = [] 

# --- RUTA PRINCIPAL (FRONTEND) ---
@app.route('/')
def index(): 

    return render_template('index.html')
 
# --- ENDPOINTS PARA TAREAS ---
  
# GET - retrieve all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():

    return jsonify({"tasks": tasks})

# POST - add a new task
@app.route("/tasks", methods=["POST"])
def add_task():

    data = request.json

    if not data or 'content' not in data or data['content'].strip() == "":
        return jsonify({"error": "No se pueden crear tareas vacías"}), 400
    
    task = {"id": len(tasks), "content": data.get("content", ""), "done": False}
    tasks.append(task)

    return jsonify({"message": "Tarea agregada!", "task": task}), 201

# PUT - update a task by ID
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):

    if task_id >= len(tasks):
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    data = request.json
    tasks[task_id]["content"] = data.get("content", tasks[task_id]["content"])
    tasks[task_id]["done"] = data.get("done", tasks[task_id]["done"])
    return jsonify({"message": "Tarea actualizada!", "task": tasks[task_id]})

# DELETE - delete a task by ID
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    if task_id >= len(tasks):
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    removed = tasks.pop(task_id)

    return jsonify({"message": "Tarea eliminada!", "task": removed})


# --- CRUD PARA USUARIOS ---

@app.route('/users', methods=['GET'])
def get_all_users():

    return jsonify({"users": users})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id >= len(users):
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(users[user_id])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json 
    
    user = {
        "id": len(users),
        "name": data.get("name"),
        "lastname": data.get("lastname", ""),
        "address": data.get("address", {
            "city": "",
            "country": "",
            "code": ""
        })
    }
    users.append(user)
    return jsonify({"message": "Usuario creado!", "user": user}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):

    if user_id >= len(users):
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    data = request.json
    users[user_id]['name'] = data.get('name', users[user_id]['name'])
    users[user_id]['lastname'] = data.get('lastname', users[user_id]['lastname'])
    users[user_id]['address'] = data.get('address', users[user_id]['address'])
     
    return jsonify({"message": "Usuario actualizado!", "user": users[user_id]})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    if user_id >= len(users):
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    removed = users.pop(user_id)
    return jsonify({"message": "Usuario eliminado!", "user": removed})

if __name__ == '__main__':
    # Ejecuta el servidor en el puerto 5000 con modo debug activado
    app.run(debug=True, port=5000)