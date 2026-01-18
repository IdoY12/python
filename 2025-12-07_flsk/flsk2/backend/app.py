import os
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "inventory.db")

def init_db():
    """Initialize the database and create the table if it doesn't exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO items (name, price) VALUES ('Banana', 3.5), ('Apple', 2.2), ('Cherry', 4.8)")
    conn.commit()
    conn.close()

# GET - Read all items
@app.route('/items', methods=['GET'])
def get_items():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in items])

# POST - Create a new item
@app.route('/items', methods=['POST'])
def add_item():
    new_data = request.json # Get data from Postman JSON body
    name = new_data.get('name')
    price = new_data.get('price')
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item added successfully"}), 201

# PUT - Update an existing item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    update_data = request.json
    name = update_data.get('name')
    price = update_data.get('price')
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (name, price, item_id))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Item {item_id} updated successfully"})

# DELETE - Delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Item {item_id} deleted successfully"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)