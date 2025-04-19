from flask import Flask



def configure_routes(app: Flask):
    """
    Configure the routes for the Flask app.

    Args:
        app (Flask): The Flask app instance.
    """
    from src.api import get_data_by_columns

    # define the route for getting data by columns
    app.add_url_rule('/api/data', view_func=get_data_by_columns, methods=['GET'])
