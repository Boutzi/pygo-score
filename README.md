# Flask API: PyGo Score

The PyGo Score API allows you to manage a leaderboard system where players' scores can be added, updated, and retrieved. This API is built with Flask and works with a MongoDB storage system for player data.

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
You can check the [Swagger Documentation](http://127.0.0.1:5000/) locally, when the server is running.

## /players/leaderboard
#### Method: GET
#### Description: Returns the full list of players with their best scores.

## /players/<int:playerId>
#### Method: GET
#### Description: Returns the player data for the specified playerId.

## /players/<string:player>/<int:best>
#### Method: PUT
#### Description: Updates the player's best score if the player exists. Adds a new player if the player is not found.

# MongoDB Config:
To use MongoDB with this API, follow these steps:

Create a ```.env``` File: Create a ```.env``` file in the project root directory. This file should contain the following environment variables:

```
ATLAS_URI=your_mongodb_connection_string
DB_NAME=your_database_name
COLLECTION_NAME=your_collection_name
```
Replace your_mongodb_connection_string, your_database_name, and your_collection_name with your actual MongoDB connection string, database name, and collection name.

### You can also deploy to Cloud Platforms: If you are deploying the API to cloud platforms like Heroku, AWS, or similar, set these environment variables in your cloud provider's configuration settings.

By following these steps, you can configure the API to work with MongoDB and ensure that it is correctly set up for both local development and cloud deployment.