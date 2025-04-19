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

def get_mean_by_columns():
    """
    Get the mean of the specified columns from the CSV file, grouped by 'genre'.
    For numeric columns, return the mean within each group.
    For non-numeric columns, return the value with the highest count within each group.
    """
    # get the columns from the request
    columns = request.args.getlist('columns')
    
    # read the CSV file
    df = pd.read_csv(config.DATASET_PATH)
    
    # ensure 'genre' column exists
    if 'genre' not in df.columns:
        return jsonify({"error": "'genre' column not found in the dataset"}), 400
    
    # group the data by 'genre'
    grouped = df.groupby('genre')
    
    # calculate the mean for numeric columns and the most frequent value for non-numeric columns
    result = {}
    for genre, group in grouped:
        result[genre] = {}
        if len(columns) > 0:
            for column in columns:
                if column in group.columns:
                    if pd.api.types.is_numeric_dtype(group[column]):
                        result[genre][column] = group[column].mean()
                    else:
                        result[genre][column] = group[column].mode()[0]  # most frequent value
        else:
            for column in group.columns:
                if pd.api.types.is_numeric_dtype(group[column]):
                    result[genre][column] = group[column].mean()
                else:
                    result[genre][column] = group[column].mode()[0]  # most frequent value
    
    return jsonify(result), 200
