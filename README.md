# Visualization dashboard for Mental Health and Music Features analysis

This project is a visualization dashboard designed to analyze the relationship between mental health and music features. It provides interactive charts and graphs to help users explore patterns and insights.

## Features

- Interactive visualizations for mental health and music data.
- Customizable filters and parameters for in-depth analysis.
- Exportable reports and charts.

## Data Processing Pipeline

The data processing pipeline is a crucial component of this project, enabling the transformation of raw datasets into a unified and analyzable format. The original dataset files are located in the `archive/` directory. By executing the `pipeline.sh` script, the following sequential steps are performed:

1. **Data Filtering**: Unnecessary features are removed from the datasets, retaining only the attributes relevant for analysis. This step ensures a focused and efficient exploration of the data.

2. **Decoupling Multi-Value Features**: Multi-value features are split into separate rows, allowing for a more granular and detailed analysis of the data.

3. **Linguistic Feature Analysis**: An NLP model is employed to standardize and map genre strings into specific categorical values, ensuring consistency and enabling meaningful comparisons.

4. **Normalization**: Numerical values are normalized to a consistent scale, facilitating better interpretability and reducing biases in the analysis.

5. **Data Merging**: All datasets are combined into a single, unified dataset, providing a comprehensive view of the data for further processing.

6. **Handling Missing Values**: Missing data points are filled using linear regression techniques, minimizing data loss and maintaining the integrity of the dataset.

7. **Duplicate Removal**: Duplicate rows are identified and removed to ensure the dataset remains clean and free of redundancy.

8. **Data Sampling and Clustering**: Principal Component Analysis (PCA) and K-means clustering are applied to group similar data points. This step reduces the dataset size by sampling representative data from each cluster, improving computational efficiency without compromising the quality of insights.

This pipeline ensures that the data is preprocessed effectively, enabling accurate and meaningful analysis in the visualization dashboard.

## How to run?

Clone the repository, enter the dashboard directory and run:

```sh
python3 -m pip install -r requirements.txt
python3 app.py --reload=True --debug=False --port=5000
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
