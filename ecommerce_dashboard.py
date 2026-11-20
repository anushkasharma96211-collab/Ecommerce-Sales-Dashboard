import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the CSV file from the dataset folder
df = pd.read_csv('dataset/ecommerce_sales_data.csv')

# 2. Data Cleaning & Inspection
print('First 5 Rows of Dataset:')
print(df.head())

print('\nDataset Shape (Rows, Columns):', df.shape)
print('\nMissing Values per Column:')
print(df.isnull().sum())

print('\nDuplicate Rows:', df.duplicated().sum())
df = df.drop_duplicates()

# 3. Overall E-Commerce KPIs
total_sales = np.sum(df['Sales'])
total_profit = np.sum(df['Profit'])
total_quantity = np.sum(df['Quantity'])
avg_order_sales = np.mean(df['Sales'])
profit_margin = (total_profit / total_sales) * 100

print('\n--- OVERALL E-COMMERCE PERFORMANCE ---')
print(f'Total Revenue (Sales):   ${total_sales:,.2f}')
print(f'Total Profit:            ${total_profit:,.2f}')
print(f'Overall Profit Margin:   {profit_margin:.2f}%')
print(f'Total Units Sold:        {total_quantity:,}')
print(f'Average Sale/Order:      ${avg_order_sales:,.2f}')

# 4. Summary Tables
category_summary = df.groupby('Category')[['Quantity', 'Sales', 'Profit']].sum().reset_index()
category_summary['Profit Margin (%)'] = (category_summary['Profit'] / category_summary['Sales']) * 100
print('\n--- SALES & PROFIT BY CATEGORY ---')
print(category_summary.sort_values(by='Sales', ascending=False))

region_summary = df.groupby('Region')[['Quantity', 'Sales', 'Profit']].sum().reset_index()
print('\n--- SALES & PROFIT BY REGION ---')
print(region_summary.sort_values(by='Profit', ascending=False))

top_products = df.groupby('Product Name')[['Quantity', 'Sales', 'Profit']].sum().reset_index()
top_5 = top_products.sort_values(by='Profit', ascending=False).head(5)
print('\n--- TOP 5 PRODUCTS BY PROFIT ---')
print(top_5)

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Month_Year'] = df['Order Date'].dt.to_period('M').astype(str)
monthly_trend = df.groupby('Month_Year')[['Sales', 'Profit']].sum().reset_index()
print('\n--- MONTHLY SALES & PROFIT TREND ---')
print(monthly_trend.head(12))

# 5. Visual Dashboard (4 Charts in 1 Window)
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle('E-Commerce Sales & Profit Dashboard', fontsize=16, fontweight='bold')

# Chart 1: Sales by Category (Top-Left)
axes[0, 0].bar(category_summary['Category'], category_summary['Sales'], color=['#2b5c8f', '#4a90e2', '#7fb3d5'])
axes[0, 0].set_title('Total Sales by Category')
axes[0, 0].set_ylabel('Sales ($)')

# Chart 2: Sales Share by Region (Top-Right)
axes[0, 1].pie(region_summary['Sales'], labels=region_summary['Region'], autopct='%1.1f%%', startangle=90)
axes[0, 1].set_title('Sales Distribution by Region')

# Chart 3: Top 5 Products by Profit (Bottom-Left)
axes[1, 0].barh(top_5['Product Name'], top_5['Profit'], color='#2e8b57')
axes[1, 0].invert_yaxis()
axes[1, 0].set_title('Top 5 Products by Profit')
axes[1, 0].set_xlabel('Profit ($)')

# Chart 4: Monthly Sales Trend (Bottom-Right)
recent_months = monthly_trend.head(12)
axes[1, 1].plot(recent_months['Month_Year'], recent_months['Sales'], marker='o', color='#d9534f')
axes[1, 1].set_title('Monthly Sales Trend')
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].set_ylabel('Sales ($)')

plt.tight_layout()
plt.show()