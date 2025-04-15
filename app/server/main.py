from flask import Flask
from flask_cors import CORS
from src import router



# create a Flask app
app = Flask(__name__, static_folder='public/static', template_folder='public')
app.config["JSON_SORT_KEYS"] = False

# set CORS middleware for the app
CORS(app)

# configure the routes
router.configure_routes(app)

# run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # set the port number here
