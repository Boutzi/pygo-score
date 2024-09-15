from flask import Flask, jsonify
import json

app = Flask(__name__)

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
            player["best"] = new_best
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
    return jsonify(players_dict)

@app.route("/players/<int:playerId>", methods=["GET"])
def get_one_player(playerId: int):
    player = players_dict[playerId]
    return jsonify(player)

@app.route("/players/<string:player>/<int:best>", methods=["PUT"])
def set_player_best_score(player: str, best: int):
    write_data(player, best)
    return jsonify({"success": True})