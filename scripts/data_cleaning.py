import pandas as pd
import os

# Paths
data_path = "data/Superstore_Sales_Full.csv"
cleaned_data_path = "data/Cleaned_Superstore_Sales.csv"

# Create output directory if not exists
output_dir = os.path.dirname(cleaned_data_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the data
df = pd.read_csv(data_path, encoding='latin1')

# Convert date columns to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Remove duplicates
df.drop_duplicates(inplace=True)

# Remove rows with missing values
df.dropna(inplace=True)

# Calculate Revenue and Profit Margin
# Assuming Revenue = Sales - Discount Amount (but your discount column is %)
# So Revenue = Sales * (1 - Discount)
df['Revenue'] = df['Sales'] * (1 - df['Discount'])

# Avoid division by zero
df['Profit Margin'] = df.apply(lambda row: row['Profit'] / row['Revenue'] if row['Revenue'] != 0 else 0, axis=1)

# Save cleaned data
df.to_csv(cleaned_data_path, index=False)

# Print info to confirm
print("\nData cleaning completed. Cleaned data saved to:", cleaned_data_path)
print("\nSample cleaned data:")
print(df.head())
print("\nData info:")
print(df.info())
