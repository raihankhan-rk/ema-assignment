import pandas as pd
import random
import string

# Function to generate a random email
def generate_random_email():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    domain = ''.join(random.choices(string.ascii_lowercase, k=5))
    return f"{username}@{domain}.com"

# Function to generate a random names
def generate_random_string():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=7))

df1 = pd.read_csv('data/Leads1.csv', encoding='iso-8859-1')
df2 = pd.read_csv('data/Leads2.csv', encoding='iso-8859-1')

# Merging the dataframes on 'Prospect ID'
combined_df = pd.merge(df1, df2, on='Prospect ID', how='outer')

# Removing duplicate columns (columns ending with '_y')
columns_to_drop = [col for col in combined_df.columns if col.endswith('_y')]
combined_df = combined_df.drop(columns=columns_to_drop)

# Renaming columns ending with '_x' by removing the '_x' suffix
combined_df.columns = [col[:-2] if col.endswith('_x') else col for col in combined_df.columns]

combined_df['First Name'] = [generate_random_string() for _ in range(len(combined_df))]
combined_df['Last Name'] = [generate_random_string() for _ in range(len(combined_df))]

# Adding new 'Email' column with NaN values
combined_df['Email'] = pd.NA

# Filling random rows with email addresses
num_rows_to_fill = len(combined_df) // 50
rows_to_fill = random.sample(range(len(combined_df)), num_rows_to_fill)
combined_df.loc[rows_to_fill, 'Email'] = [generate_random_email() for _ in range(num_rows_to_fill)]


filtered_df = combined_df[
    (combined_df['Company'].notna()) | (combined_df['Email'].notna())
]

total_filtered_leads = len(filtered_df)

filtered_df.to_csv('filtered_leads.csv', index=False, encoding='utf-8')

print(f"Total number of leads with company or email: {total_filtered_leads}")
print("Filtered leads have been saved to 'filtered_leads.csv'")

print(filtered_df.head())