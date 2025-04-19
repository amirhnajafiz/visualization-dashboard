from flask import request, jsonify
import pandas as pd

from src import config



def get_data_by_columns():
    """
    Get data from the CSV file based on the specified columns with pagination.
    """
    # get the columns from the request
    columns = request.args.getlist('columns')
    
    # get pagination parameters
    page = int(request.args.get('page', 1))  # default to page 1
    per_page = 100  # fixed items per page
    
    # read the CSV file
    df = pd.read_csv(config.DATASET_PATH)
    
    # filter the DataFrame based on the specified columns
    if len(columns) > 0:
        filtered_df = df[columns]
    else:
        filtered_df = df
    
    # apply pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated_df = filtered_df.iloc[start:end]
    
    return jsonify({
        "records": paginated_df.to_dict(orient='records'),
        "page": page,
        "per_page": per_page,
        "total_pages": (len(filtered_df) + per_page - 1) // per_page,
    }), 200
