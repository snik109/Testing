from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

API_KEY = "mysecretapikey123"  # Set your API key here

DATA_FILE = 'data.json'

# Load existing data if the file exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        data_store = json.load(f)
else:
    data_store = {"items": []}

# Function to save data to file
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data_store, f, indent=2)

# 🔒 Helper function to check API key
def check_api_key():
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return False
    return True

@app.route('/')
def home():
    return "Welcome to your first API!"

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data_store["items"])

@app.route('/items', methods=['POST'])
def add_item():
    if not check_api_key():  # Check if API key is provided
        return jsonify({"error": "Unauthorized"}), 401
    items = request.json.get('items')
    if items and isinstance(items, list):
        data_store["items"].extend(items)
        save_data()
        return jsonify({"message": "Items added", "items": items}), 201
    return jsonify({"error": "No valid items provided"}), 400

@app.route('/items/<int:index>', methods=['DELETE'])
def delete_item(index):
    if not check_api_key():  # Check if API key is provided
        return jsonify({"error": "Unauthorized"}), 401
    try:
        removed_item = data_store["items"].pop(index)
        save_data()
        return jsonify({"message": "Item deleted", "item": removed_item})
    except IndexError:
        return jsonify({"error": "Invalid index"}), 400

if __name__ == '__main__':
    app.run()
