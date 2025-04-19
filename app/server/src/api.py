from flask import request, jsonify
import pandas as pd

from src import config



def get_data_by_columns():
    """
    Get data from the CSV file based on the specified columns.
    """
    # get the columns from the request
    columns = request.args.getlist('columns')
    
    # read the CSV file
    df = pd.read_csv(config.DATASET_PATH)
    
    # filter the DataFrame based on the specified columns
    if len(columns) > 0:
        filtered_df = df[columns]
    else:
        filtered_df = df
    
    return jsonify(filtered_df.to_dict(orient='records'))
