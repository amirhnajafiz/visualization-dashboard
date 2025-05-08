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

# parameters
max_rows_per_country = 300
min_rows_per_country = 20

# get the counts of rows per country
country_counts = df['country'].value_counts()

# find countries that need more rows to reach the minimum threshold
countries_needing_rows = country_counts[country_counts < min_rows_per_country].index.tolist()

# find countries that exceed the maximum threshold
countries_exceeding_rows = country_counts[country_counts > max_rows_per_country].index.tolist()

# redistribute rows from overrepresented countries to underrepresented ones
for country in countries_exceeding_rows:
    # get rows for the overrepresented country
    excess_rows = df[df['country'] == country]
    excess_count = len(excess_rows) - max_rows_per_country

    # randomly select rows to redistribute
    rows_to_redistribute = excess_rows.sample(n=excess_count)

    for index, row in rows_to_redistribute.iterrows():
        # check if there are still countries needing rows
        if not countries_needing_rows:
            break

        # randomly assign to a country that needs more rows
        target_country = random.choice(countries_needing_rows)
        df.at[index, 'country'] = target_country

        # update counts
        country_counts[target_country] += 1
        country_counts[country] -= 1

        # if the target country reaches the minimum threshold, remove it from the list
        if country_counts[target_country] >= min_rows_per_country:
            countries_needing_rows.remove(target_country)

        # if the source country drops below the maximum threshold, stop redistributing
        if country_counts[country] <= max_rows_per_country:
            break

# verify the result
print(df['country'].value_counts())

# save the dataset
df.to_csv('assets/datasets/dataset.csv', index=False)
