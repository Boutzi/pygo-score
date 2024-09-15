from flask import Flask, abort
from flask_restx import Api, Resource, Namespace
import os
from mongodb_client import AtlasClient
from dotenv import load_dotenv

load_dotenv()

ATLAS_URI = os.getenv("ATLAS_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if not ATLAS_URI or not DB_NAME or not COLLECTION_NAME:
    raise ValueError("Environment variables ATLAS_URI, DB_NAME, or COLLECTION_NAME are not defined.")

app = Flask(__name__)
api = Api(app, version='1.0', title='PyGo Score API',
          description='A simple API for managing player scores in PyGo')

player_ns = Namespace('players', description='Players management')
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'

atlas_client = AtlasClient(ATLAS_URI, DB_NAME)
atlas_client.ping()
print('Connected to Atlas instance! We are good to go!')

@player_ns.route('/leaderboard')
class Leaderboard(Resource):
    def get(self):
        players = atlas_client.find(COLLECTION_NAME, {}, limit=0)
        for player in players:
            player['_id'] = str(player.get('_id')) 
        return players

@player_ns.route('/<int:playerId>')
class Player(Resource):
    def get(self, playerId):
        player = atlas_client.find(COLLECTION_NAME, {"_id": playerId}, limit=1)
        if player:
            player = player[0]
            player['_id'] = str(player.get('_id')) 
            return player
        abort(404, description="Player not found")
        
@player_ns.route('/<string:player>/<int:best>')
class PlayerBestScore(Resource):
    def put(self, player, best):
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


api.add_namespace(player_ns)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
