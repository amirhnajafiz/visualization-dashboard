import pandas as pd



# read the dataset as CSV
df = pd.read_csv('dashboard/data/dataset.csv')

# print the number of columns and rows
print(f"Number of columns: {df.shape[1]}")
print(f"Number of rows: {df.shape[0]}")

# print the number of unique values in each column
print("Number of unique values in each column:")
print(df.nunique())

# print number of items per each country
print("Number of items per each country:")
print(df['country'].value_counts())

# print the top 5 rows of the dataset
print("Top 5 rows of the dataset:")
print(df.head())
