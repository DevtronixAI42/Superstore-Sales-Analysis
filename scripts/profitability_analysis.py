import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
cleaned_data_path = "data/Cleaned_Superstore_Sales.csv"
output_csv_path = "data/profitability_summary.csv"
plots_dir = "plots"

# Ensure output directories exist
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

# Load cleaned data
df = pd.read_csv(cleaned_data_path)

# Group by Category and Sub-Category, aggregate sum of Profit and Revenue
profit_summary = df.groupby(['Category', 'Sub-Category']).agg({
    'Profit': 'sum',
    'Revenue': 'sum'
}).reset_index()

# Calculate Profit Margin (%)
profit_summary['Profit Margin %'] = (profit_summary['Profit'] / profit_summary['Revenue']) * 100

# Save summary to CSV
profit_summary.to_csv(output_csv_path, index=False)
print(f"Profitability summary saved to '{output_csv_path}'.")

# Plot total profit by Category
plt.figure(figsize=(10,6))
category_profit = profit_summary.groupby('Category')['Profit'].sum()
category_profit.plot(kind='bar', color='seagreen')
plt.title('Total Profit by Category')
plt.ylabel('Profit')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'total_profit_by_category.png'))
plt.show()

# Plot profit margin by Sub-Category (top 10 by profit)
top_subcategories = profit_summary.sort_values(by='Profit', ascending=False).head(10)
plt.figure(figsize=(12,6))
plt.bar(top_subcategories['Sub-Category'], top_subcategories['Profit Margin %'], color='coral')
plt.title('Profit Margin % of Top 10 Sub-Categories by Profit')
plt.ylabel('Profit Margin (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'profit_margin_top_subcategories.png'))
plt.show()

# Optional: Print top 5 profitable sub-categories summary
print("Top 5 Sub-Categories by Profit:")
print(top_subcategories[['Sub-Category', 'Profit', 'Profit Margin %']].head())
