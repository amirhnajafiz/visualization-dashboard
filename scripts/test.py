import pandas as pd



# read the original dataset
df = pd.read_csv("dashboard/data/dataset.csv")

# select random 100 rows
df = df.sample(n=25, random_state=1)

# save the new dataset
df.to_csv("dashboard/data/test.csv", index=False)
