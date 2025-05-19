import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
cleaned_data_path = "data/Cleaned_Superstore_Sales.csv"
output_dir = "plots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load cleaned data
df = pd.read_csv(cleaned_data_path)

# Convert 'Order Date' to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Extract Year-Month for grouping
df['YearMonth'] = df['Order Date'].dt.to_period('M')

# **Overall Sales Trend**
monthly_sales = df.groupby('YearMonth')['Revenue'].sum().reset_index()
monthly_sales['YearMonth'] = monthly_sales['YearMonth'].dt.to_timestamp()


plt.figure(figsize=(12,6))
plt.plot(monthly_sales['YearMonth'], monthly_sales['Revenue'], marker='o', color='green')
plt.title('Overall Monthly Revenue Trend')
plt.xlabel('Year-Month')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'overall_sales_trend.png'))
plt.show()

# **Category-wise Sales Trend**
category_sales = df.groupby(['YearMonth', 'Category'])['Revenue'].sum().unstack()

category_sales.plot(figsize=(12,6), marker='o')
plt.title('Monthly Revenue Trend by Product Category')
plt.xlabel('Year-Month')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'category_sales_trend.png'))
plt.show()

# Save overall sales trend data
monthly_sales.to_csv("data/overall_sales_trends.csv", index=False)

# Save category-wise sales trend data
category_sales.reset_index().to_csv("data/category_sales_trends.csv", index=False)
