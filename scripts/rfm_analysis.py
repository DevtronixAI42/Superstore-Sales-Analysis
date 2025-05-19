import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
cleaned_data_path = "data/Cleaned_Superstore_Sales.csv"
output_csv_path = "data/rfm_scores.csv"
plots_dir = "plots"

# Create output directories if they don't exist
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

# Load cleaned data
df = pd.read_csv(cleaned_data_path)

# Convert 'Order Date' to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Reference date for Recency calculation: max order date + 1 day
reference_date = df['Order Date'].max() + pd.Timedelta(days=1)

# Calculate RFM metrics
rfm = df.groupby('Customer ID').agg({
    'Order Date': lambda x: (reference_date - x.max()).days,  # Recency
    'Order ID': 'nunique',  # Frequency
    'Revenue': 'sum'        # Monetary
}).reset_index()

rfm.rename(columns={
    'Order Date': 'Recency',
    'Order ID': 'Frequency',
    'Revenue': 'Monetary'
}, inplace=True)

# Filter out customers with zero or negative Monetary value
rfm = rfm[rfm['Monetary'] > 0]

# Score Recency (lower is better, so reversed labels)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1]).astype(int)

# Score Frequency (higher is better)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)

# Score Monetary (higher is better)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5]).astype(int)

# Combine RFM score as string
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# Assign customer segments based on RFM scores
def assign_rfm_segment(row):
    if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return 'Champions'
    elif row['F_Score'] >= 4 and row['R_Score'] < 4:
        return 'Loyal Customers'
    elif row['R_Score'] >= 3 and row['F_Score'] >= 3 and row['M_Score'] < 4:
        return 'Potential Loyalists'
    elif row['R_Score'] <= 2 and row['F_Score'] >= 3:
        return 'At Risk'
    elif row['R_Score'] <= 2 and row['F_Score'] <= 2:
        return 'Lost'
    else:
        return 'Others'

rfm['Segment'] = rfm.apply(assign_rfm_segment, axis=1)

# Save the RFM scores to CSV
rfm.to_csv(output_csv_path, index=False)
print(f"RFM analysis completed. Results saved to '{output_csv_path}'.")

# Plot customer counts by segment
plt.figure(figsize=(10,6))
rfm['Segment'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Customer Count by Segment')
plt.xlabel('Segment')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "rfm_customer_segments.png"))
plt.show()

# Print and optionally save summary stats per segment
segment_summary = rfm.groupby('Segment').agg({
    'Customer ID': 'count',
    'Monetary': ['mean', 'sum'],
    'Frequency': 'mean',
    'Recency': 'mean'
}).rename(columns={'Customer ID': 'Customer Count'})

print(segment_summary)

# Save segment summary CSV (optional)
segment_summary.to_csv("data/rfm_segment_summary.csv")
