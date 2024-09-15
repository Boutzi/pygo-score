from flask import Flask, jsonify
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

# db_mode = mongo | db_mode = local
db_mode = "mongo" 

app = Flask(__name__)

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db_name = "pygo_score"
db = client[db_name]
players_collection = db.players

input_file = "./players.json"
def read_json():
    with open(input_file, encoding="utf-8") as json_file:
        return json.load(json_file)
    
def write_json(data):
    with open(input_file, 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

parsed_json = read_json()

def extract_data(json_data):
    extracted_data = {}
    for player in json_data["players"]:
        extracted_data[player["id"]] = {
            "name": player["name"],
            "best": player["best"]
        }
    return extracted_data
    
players_dict = extract_data(parsed_json)

def write_data(player_name, new_best):
    global parsed_json
    player_exists = False
    for player in parsed_json["players"]:
        if player["name"].upper() == player_name.upper():
            if player["best"] < int(new_best):
                player["best"] = int(new_best)
                player_exists = True
                break
            else:
                player_exists = True
                break
    if not player_exists:
        new_id = max([p["id"] for p in parsed_json["players"]]) + 1
        new_player = {
        "id": new_id,
        "name": player_name.upper(),
        "best": new_best
        }
        parsed_json["players"].append(new_player)
    write_json(parsed_json)

@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    if db_mode == "mongo":
        players = list(players_collection.find({}, {"_id": 0}))
        return jsonify(players)
    elif db_mode == "local":
        return jsonify(players_dict)
    else:
        return "Error: db_mode unknown"

@app.route("/players/<int:playerId>", methods=["GET"])
def get_one_player(playerId: int):
    if db_mode == "mongo":
        player = players_collection.find_one({"id": playerId}, {"_id": 0})
        if player:
            return jsonify(player)
        return jsonify({"error": "Player not found"}), 404
    elif db_mode == "local":
        player = players_dict[playerId]
        return jsonify(player)
    else:
        return "Error: db_mode unknown"

@app.route("/players/<string:player>/<int:best>", methods=["PUT"])
def set_player_best_score(player: str, best: int):
    if db_mode == "mongo":
        player_data = players_collection.find_one({"name": player.upper()})
        if player_data:
            if player_data["best"] < best:
                players_collection.update_one({"name": player.upper()}, {"$set": {"best": best}})
        else:
            new_id = players_collection.count_documents({}) + 1
            new_player = {
                "id": new_id,
                "name": player.upper(),
                "best": best
        }
        players_collection.insert_one(new_player)
        return jsonify({"success": True})
    elif db_mode == "local":
        write_data(player, best)
        return jsonify({"success": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)