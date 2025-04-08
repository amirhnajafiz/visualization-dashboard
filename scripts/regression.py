import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression



# load the dataset
df = pd.read_csv("mxmh_survey_results.csv")

# check the current number of rows
current_rows = len(df)
target_rows = 1000

# generate synthetic data
if current_rows < target_rows:
    # separate numerical and categorical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns

    # train regression models for numerical columns
    regression_models = {}
    for col in numerical_cols:
        # use other numerical columns as predictors
        predictors = [c for c in numerical_cols if c != col]
        if predictors:
            # drop rows with missing values in predictors or target column
            X = df[predictors]
            y = df[col]
            valid_rows = X.notna().all(axis=1) & y.notna()
            X = X[valid_rows]
            y = y[valid_rows]
            
            if len(X) > 0:  # ensure there is enough data to train the model
                model = LinearRegression()
                model.fit(X, y)
                regression_models[col] = (model, predictors)

    # generate new samples
    new_samples = []
    for _ in range(target_rows - current_rows):
        new_sample = {}
        
        # generate categorical values based on frequency distribution
        for col in categorical_cols:
            value_counts = df[col].value_counts(normalize=True)
            new_sample[col] = np.random.choice(value_counts.index, p=value_counts.values)
        
        # generate numerical values using regression models
        for col, (model, predictors) in regression_models.items():
            predictor_values = {p: new_sample[p] for p in predictors if p in new_sample}
            if len(predictor_values) == len(predictors):
                X_new = np.array([predictor_values[p] for p in predictors]).reshape(1, -1)
                new_sample[col] = model.predict(X_new)[0]
            else:
                # fallback to random sampling if predictors are missing
                new_sample[col] = np.random.uniform(df[col].min(), df[col].max())
        
        new_samples.append(new_sample)
    
    # convert new samples to a DataFrame
    additional_samples = pd.DataFrame(new_samples)
    
    # append the new samples to the original dataset
    df_expanded = pd.concat([df, additional_samples], ignore_index=True)
else:
    df_expanded = df

# save the expanded dataset
df_expanded.to_csv("mxmh_survey_results_expanded.csv", index=False)

print(f"Dataset expanded to {len(df_expanded)} rows and saved as 'mxmh_survey_results_expanded.csv'.")
