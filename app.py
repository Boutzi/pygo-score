from flask import Flask, jsonify, abort
from flask_restx import Api, Resource
import json
import os
from mongodb_client import AtlasClient

# db_mode = mongo | db_mode = local
db_mode = "mongo"

ATLAS_URI = os.getenv("ATLAS_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if not ATLAS_URI or not DB_NAME:
    raise ValueError("Environment variables ATLAS_URI, DB_NAME, or COLLECTION_NAME are not defined.")

app = Flask(__name__)
api = Api(app, version='1.0', title='PyGo Score API',
          description='A simple API for managing player scores in PyGo')

atlas_client = AtlasClient(ATLAS_URI, DB_NAME)
atlas_client.ping()
print('Connected to Atlas instance! We are good to go!')

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

@api.route('/leaderboard')
class Leaderboard(Resource):
    def get(self):
        if db_mode == "mongo":
            players = atlas_client.find(COLLECTION_NAME, {}, limit=0)
            for player in players:
                player['_id'] = str(player.get('_id')) 
            return players
        elif db_mode == "local":
            return players_dict
        else:
            abort(400, description="Error: db_mode unknown")

@api.route('/players/<int:playerId>')
class Player(Resource):
    def get(self, playerId):
        if db_mode == "mongo":
            player = atlas_client.find(COLLECTION_NAME, {"id": playerId}, limit=1)
            if player:
                player = player[0]
                player['_id'] = str(player.get('_id')) 
                return player
            abort(404, description="Player not found")
        elif db_mode == "local":
            player = players_dict.get(playerId)
            if player:
                return player
            abort(404, description="Player not found")
        else:
            abort(400, description="Error: db_mode unknown")

@api.route('/players/<string:player>/<int:best>')
class PlayerBestScore(Resource):
    def put(self, player, best):
        if db_mode == "mongo":
            player_data = atlas_client.find(COLLECTION_NAME, {"name": player.upper()})
            if player_data:
                player_data = player_data[0]
                if player_data["best"] < best:
                    atlas_client.database[COLLECTION_NAME].update_one({"name": player.upper()}, {"$set": {"best": best}})
            else:
                new_player = {
                    "name": player.upper(),
                    "best": best
                }
                atlas_client.database[COLLECTION_NAME].insert_one(new_player)
            return {"success": True}
        elif db_mode == "local":
            write_data(player, best)
            return {"success": True}
        else:
            abort(400, description="Error: db_mode unknown")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
