import pandas as pd
import random



# read the dataset
df = pd.read_csv('assets/datasets/dataset.csv')

# make 'mode' column values either 0 or 1, they are currently between 0 and 1
df['mode'] = df['mode'].apply(lambda x: 1 if x > 0.5 else 0)

# make 'age' column an integer
df['age'] = df['age'].apply(lambda x: int(x))

# for all numeric columns, if they have a decimal point, set them to 2 decimal points
for col in df.select_dtypes(include=['float64']).columns:
    df[col] = df[col].apply(lambda x: round(x, 2))

# make 'age' columns greater than 65 to random number between 20 and 80
df['age'] = df['age'].apply(lambda x: random.randint(20, 80) if x > 65 else x)

# save the dataset
df.to_csv('assets/datasets/dataset.csv', index=False)
