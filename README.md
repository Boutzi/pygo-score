# Flask API: PyGo Score

The PyGo Score API allows you to manage a leaderboard system where players' scores can be added, updated, and retrieved. This API is built with Flask and works with a JSON-based storage system for player data.

# Installation:
First, install Python.
Then open the console, navigate to the folder of your choice, and clone this repository:

```
git clone https://github.com/Boutzi/pygo-score.git
```
Navigate to the repo folder and create a new virtual environment:
```
python -m venv env
```
Next, activate it.
For Windows:
```
env\scripts\activate.bat
```
For Linux:
```
source env/bin/activate
```
Now, install the required packages:
```
pip install -r requirements.txt
```
Finally, you can run the script:
```
python main.py
```
The API will be available at ```http://127.0.0.1:5000```

# API Endpoints

## /leaderboard
#### Method: GET
#### Description: Returns the full list of players with their best scores.

## /players/<int:playerId>
#### Method: GET
#### Description: Returns the player data for the specified playerId.

## /players/<string:player>/<int:best>
#### Method: PUT
#### Description: Updates the player's best score if the player exists. Adds a new player if the player is not found.

# Config:
You can configure the initial player data and other settings by modifying the players.json file, which holds all player information. The structure looks like this:
```json
{
  "players": [
    {
      "id": 1,
      "name": "PLAYER1",
      "best": 29
    },
    {
      "id": 2,
      "name": "PLAYER2",
      "best": 23
    },
    {
      "id": 3,
      "name": "PLAYER3",
      "best": 100
    }
  ]
}
```
JSON File Management
If you wish to pre-load or update player data manually, edit the players.json file located in the project folder. The API automatically reads and writes to this file when new players are added or scores updated.