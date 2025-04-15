from flask import Flask
from flask_cors import CORS
from src import router



# create a Flask app
app = Flask(__name__, static_folder='public/static', template_folder='public')

# Flask app configurations
app.config["JSON_SORT_KEYS"] = False
app.config["DEBUG"] = True

# set CORS middleware for the app with specific origins
CORS(app, resources={r"/*": {"origins": "*"}})

# configure the routes
router.configure_routes(app)

# run the app
if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=5000)  # set the port number here
