import pandas as pd
import numpy as np++
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the data
data = """Order_ID,Customer_ID,Customer_Name,Country,Order_Date,Ship_Date,Product_Category,Product_Name,Quantity,Unit_Price,Discount,Shipping_Cost,Payment_Method,Order_Status,Customer_Rating,Warehouse,Returned,Sales_Rep,Profit
1001,C001,John Smith,USA,2025-01-05,2025-01-08,Electronics,Laptop Pro 15,2,1200,0.10,25,Credit Card,Delivered,5,WH-A,No,Alice Johnson,350
1002,C002,Sarah Lee,UK,05/01/2025,2025-01-09,Furniture,Office Chair,1,350,5%,40,PayPal,Delivered,4,WH-B,No,Bob Miller,120
1003,C003,Mike Brown,India,2025/01/07,2025-01-15,Electronics,Wireless Mouse,5,25,NULL,15,Cash,Returned,2,WH-A,Yes,Charlie Green,-20
1004,C004,Emily Davis,Germany,2025-13-08,2025-01-16,Clothing,Jacket,3,80,0.15,20,Credit Card,Delivered,?,WH-C,No,Alice Johnson,60
1005,C005,Chris Wilson,USA,2025-01-10,2025-01-09,Electronics,Monitor 27inch,-2,300,0.05,30,Credit Card,Cancelled,3,WH-A,No,,100
1006,C006,Anna Taylor,Canada,2025-01-11,2025-01-20,Furniture,Standing Desk,1,abc,0.2,50,Debit Card,Delivered,5,WH-B,No,Bob Miller,200
1007,C007,David Clark,USA,2025-01-12,2025-01-18,Electronics,Keyboard Mechanical,4,110,0.1,18,Crypto,Delivered,4,WH-A,No,Alice Johnson,90
1008,C008,Jessica Hall,France,2025-01-13,NULL,Clothing,Sneakers,2,95,0.05,22,Credit Card,In Transit,NaN,WH-C,No,Charlie Green,70
1009,C009,Daniel Young,India,15-01-2025,2025-01-25,Furniture,Bookshelf,1,210,0,35,UPI,Delivered,5,WH-B,No,Bob Miller,110
1010,C010,Sophia King,USA,2025-01-16,2025-01-17,Electronics,Tablet Air,3,450,0.50,25,Credit Card,Delivered,1,WH-X,No,Alice Johnson,-500
1011,C011,James Scott,Australia,2025-01-17,2025-01-22,Clothing,T-Shirt Pack,10,15,0.05,10,PayPal,Delivered,4,WH-C,No,Charlie Green,40
1012,C012,Olivia Green,USA,2025-01-18,2025-01-28,Furniture,Sofa Set,1,1500,0.25,120,Credit Card,Fraud,5,WH-B,No,Bob Miller,800
1013,C013,Liam Baker,USA,2025-01-19,2025-01-26,Electronics,Smartphone X,2,9999,0.01,35,Credit Card,Delivered,5,WH-A,No,Alice Johnson,9500
1014,C014,Emma Adams,UK,2025-01-20,2025-01-29,Clothing,Winter Coat,1,180,0.10,20,PayPal,Delivered,3,WH-C,Returned,Charlie Green,50
1015,C015,Noah Turner,India,2025-01-21,2025-01-23,Furniture,Coffee Table,1,130,,18,Cash,Delivered,4,WH-B,No,Bob Miller,45
1016,C016,John Smith,USA,2025-01-05,2025-01-08,Electronics,Laptop Pro 15,2,1200,0.10,25,Credit Card,Delivered,5,WH-A,No,Alice Johnson,350
1017,C017,Ava White,Brazil,2025-01-24,2025-02-02,Electronics,Headphones,3,75,-0.1,12,Debit Card,Delivered,4,WH-A,No,Alice Johnson,55
1018,C018,Ethan Harris,USA,2025-01-25,2025-01-24,Furniture,Bed Frame,1,700,0.15,60,Credit Card,Cancelled,2,WH-B,No,Bob Miller,-80
1019,C019,Mia Walker,Canada,2025-01-26,2025-02-01,Clothing,Hoodie,4,60,0.05,15,PayPal,Delivered,6,WH-C,No,Charlie Green,65
1020,C020,Lucas Martin,Germany,2025-01-27,2025-02-05,Electronics,Gaming Console,1,5000%,0.10,40,Credit Card,Delivered,4,WH-A,No,Alice Johnson,300
1021,C021,Grace Lee,USA,2025-01-28,2025-02-03,Furniture,Dining Table,1,950,0.2,75,Credit Card,Delivered,4,WH-B,No,Bob Miller,220
1022,C022,Henry Moore,India,2025-01-29,2025-02-06,Electronics,USB Cable,20,5,0,5,Cash,Delivered,5,WH-A,No,Alice Johnson,25
1023,C023,Charlotte King,UK,2025-01-30,2025-02-07,Clothing,Jeans,2,70,0.05,15,PayPal,Delivered,NULL,WH-C,No,Charlie Green,35
1024,C024,Benjamin Hall,USA,2025-01-31,2025-02-08,Furniture,Mattress,1,850,0.3,90,Credit Card,Delivered,4,WH-B,No,Bob Miller,180
1025,C025,Amelia Scott,France,2025-02-01,2025-02-10,Electronics,Smartwatch,2,250,0.15,18,Credit Card,Delivered,3,WH-A,No,Alice Johnson,95"""

from io import StringIO
df = pd.read_csv(StringIO(data))

print("="*80)
print("ORIGINAL DATA INFO")
print("="*80)
print(f"Shape: {df.shape}")
print(df.head(10))
print("\n")

# ============================================
# DATA CLEANING FUNCTIONS
# ============================================

def clean_data(df):
    df_clean = df.copy()
    
    # 1. Remove duplicates
    df_clean = df_clean.drop_duplicates(subset=['Order_ID'])
    
    # 2. Clean Quantity (remove negative values)
    df_clean['Quantity'] = pd.to_numeric(df_clean['Quantity'], errors='coerce')
    df_clean['Quantity'] = df_clean['Quantity'].clip(lower=0)
    df_clean['Quantity'].fillna(df_clean['Quantity'].median(), inplace=True)
    
    # 3. Clean Unit_Price (remove % signs and invalid values)
    df_clean['Unit_Price'] = df_clean['Unit_Price'].astype(str).str.replace('%', '')
    df_clean['Unit_Price'] = pd.to_numeric(df_clean['Unit_Price'], errors='coerce')
    df_clean['Unit_Price'].fillna(df_clean['Unit_Price'].median(), inplace=True)
    df_clean.loc[df_clean['Unit_Price'] > 10000, 'Unit_Price'] = df_clean['Unit_Price'].median()
    
    # 4. Clean Discount (convert percentages to decimals)
    df_clean['Discount'] = df_clean['Discount'].astype(str).str.replace('%', '')
    df_clean['Discount'] = pd.to_numeric(df_clean['Discount'], errors='coerce')
    df_clean.loc[df_clean['Discount'] > 1, 'Discount'] = df_clean['Discount'] / 100
    df_clean['Discount'].fillna(0, inplace=True)
    df_clean['Discount'] = df_clean['Discount'].clip(lower=0)
    
    # 5. Clean Shipping_Cost
    df_clean['Shipping_Cost'] = pd.to_numeric(df_clean['Shipping_Cost'], errors='coerce')
    df_clean['Shipping_Cost'].fillna(df_clean['Shipping_Cost'].median(), inplace=True)
    df_clean['Shipping_Cost'] = df_clean['Shipping_Cost'].clip(lower=0)
    
    # 6. Clean Profit
    df_clean['Profit'] = pd.to_numeric(df_clean['Profit'], errors='coerce')
    df_clean['Profit'].fillna(df_clean['Profit'].median(), inplace=True)
    
    # 7. Clean Customer_Rating
    df_clean['Customer_Rating'] = pd.to_numeric(df_clean['Customer_Rating'], errors='coerce')
    df_clean['Customer_Rating'] = df_clean['Customer_Rating'].clip(1, 5)
    df_clean['Customer_Rating'].fillna(df_clean['Customer_Rating'].median(), inplace=True)
    
    # 8. Clean Dates
    def parse_date(date_str):
        if pd.isna(date_str) or date_str == 'NULL':
            return np.nan
        date_str = str(date_str).strip()
        formats = ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y']
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue
        return np.nan
    
    df_clean['Order_Date'] = df_clean['Order_Date'].apply(parse_date)
    df_clean['Ship_Date'] = df_clean['Ship_Date'].apply(parse_date)
    
    # Remove invalid dates
    df_clean = df_clean.dropna(subset=['Order_Date'])
    
    # Calculate shipping delay
    df_clean['Shipping_Delay'] = (df_clean['Ship_Date'] - df_clean['Order_Date']).dt.days
    df_clean['Shipping_Delay'].fillna(0, inplace=True)
    df_clean['Shipping_Delay'] = df_clean['Shipping_Delay'].clip(lower=0)
    
    # 9. Clean Payment_Method (standardize)
    df_clean['Payment_Method'] = df_clean['Payment_Method'].replace('Crypto', 'Other')
    df_clean['Payment_Method'] = df_clean['Payment_Method'].replace('UPI', 'Digital Wallet')
    
    # 10. Clean Order_Status
    df_clean['Order_Status'] = df_clean['Order_Status'].fillna('Unknown')
    
    # 11. Clean Returned
    df_clean['Returned'] = df_clean['Returned'].fillna('No')
    
    # 12. Clean Sales_Rep
    df_clean['Sales_Rep'] = df_clean['Sales_Rep'].fillna('Unassigned')
    
    # 13. Clean Country and Warehouse
    df_clean['Country'] = df_clean['Country'].fillna('Unknown')
    df_clean['Warehouse'] = df_clean['Warehouse'].fillna('Unknown')
    
    # 14. Calculate Revenue and Profit Margin
    df_clean['Revenue'] = df_clean['Quantity'] * df_clean['Unit_Price'] * (1 - df_clean['Discount'])
    df_clean['Profit_Margin'] = (df_clean['Profit'] / df_clean['Revenue']) * 100
    df_clean['Profit_Margin'] = df_clean['Profit_Margin'].replace([np.inf, -np.inf], 0)
    
    return df_clean

# Clean the data
df_clean = clean_data(df)

print("="*80)
print("CLEANED DATA INFO")
print("="*80)
print(f"Shape: {df_clean.shape}")
print("\nMissing Values:")
print(df_clean.isnull().sum())
print("\nData Types:")
print(df_clean.dtypes)
print("\nStatistical Summary:")
print(df_clean[['Quantity', 'Unit_Price', 'Profit', 'Revenue', 'Profit_Margin']].describe())

# ============================================
# GRAPH REPRESENTATIONS
# ============================================

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create comprehensive dashboard
fig = plt.figure(figsize=(20, 14))
fig.suptitle('Sales & Profit Analytics Dashboard', fontsize=18, fontweight='bold', y=0.98)

# 1. Profit by Product Category
ax1 = plt.subplot(3, 3, 1)
cat_profit = df_clean.groupby('Product_Category')['Profit'].sum().sort_values()
bars1 = ax1.barh(cat_profit.index, cat_profit.values, color='skyblue')
ax1.set_xlabel('Total Profit ($)')
ax1.set_title('Total Profit by Product Category')
for bar in bars1:
    width = bar.get_width()
    ax1.text(width, bar.get_y() + bar.get_height()/2, f'${width:,.0f}', 
             ha='left', va='center', fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# 2. Revenue vs Profit Scatter
ax2 = plt.subplot(3, 3, 2)
scatter = ax2.scatter(df_clean['Revenue'], df_clean['Profit'], 
                     c=df_clean['Profit_Margin'], cmap='RdYlGn', 
                     s=df_clean['Quantity']*20, alpha=0.6, edgecolors='black', linewidth=1)
ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax2.axvline(x=0, color='red', linestyle='--', alpha=0.5)
ax2.set_xlabel('Revenue ($)')
ax2.set_ylabel('Profit ($)')
ax2.set_title('Revenue vs Profit Analysis\n(Color: Profit Margin, Size: Quantity)')
plt.colorbar(scatter, ax=ax2, label='Profit Margin (%)')
ax2.grid(alpha=0.3)

# 3. Shipping Delay Distribution
ax3 = plt.subplot(3, 3, 3)
df_clean['Shipping_Delay'].hist(bins=20, edgecolor='black', alpha=0.7, color='lightcoral')
ax3.set_xlabel('Shipping Delay (Days)')
ax3.set_ylabel('Frequency')
ax3.set_title('Shipping Delay Distribution')
ax3.axvline(df_clean['Shipping_Delay'].mean(), color='blue', linestyle='--', 
           linewidth=2, label=f'Mean: {df_clean["Shipping_Delay"].mean():.1f} days')
ax3.legend()
ax3.grid(alpha=0.3)

# 4. Top 10 Products by Revenue
ax4 = plt.subplot(3, 3, 4)
top_products = df_clean.groupby('Product_Name')['Revenue'].sum().nlargest(10)
bars2 = ax4.barh(range(len(top_products)), top_products.values, color='lightgreen')
ax4.set_yticks(range(len(top_products)))
ax4.set_yticklabels(top_products.index, fontsize=8)
ax4.set_xlabel('Total Revenue ($)')
ax4.set_title('Top 10 Products by Revenue')
ax4.grid(axis='x', alpha=0.3)

# 5. Profit Margin by Order Status
ax5 = plt.subplot(3, 3, 5)
status_margin = df_clean.groupby('Order_Status')['Profit_Margin'].mean()
colors = ['red' if x < 0 else 'green' for x in status_margin.values]
status_margin.plot(kind='bar', ax=ax5, color=colors)
ax5.set_xlabel('Order Status')
ax5.set_ylabel('Average Profit Margin (%)')
ax5.set_title('Profit Margin by Order Status')
ax5.tick_params(axis='x', rotation=45)
ax5.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax5.grid(axis='y', alpha=0.3)

# 6. Customer Rating vs Profit
ax6 = plt.subplot(3, 3, 6)
df_clean.boxplot(column='Profit', by='Customer_Rating', ax=ax6)
ax6.set_xlabel('Customer Rating')
ax6.set_ylabel('Profit ($)')
ax6.set_title('Profit Distribution by Customer Rating')
ax6.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax6.grid(alpha=0.3)

# 7. Payment Method Analysis
ax7 = plt.subplot(3, 3, 7)
payment_data = df_clean.groupby('Payment_Method').agg({
    'Revenue': 'sum',
    'Profit': 'sum'
}).sort_values('Revenue', ascending=True)
x_pos = range(len(payment_data))
width = 0.35
bars3 = ax7.barh(x_pos, payment_data['Revenue'], width, label='Revenue', color='skyblue')
bars4 = ax7.barh([i + width for i in x_pos], payment_data['Profit'], width, label='Profit', color='lightcoral')
ax7.set_yticks([i + width/2 for i in x_pos])
ax7.set_yticklabels(payment_data.index)
ax7.set_xlabel('Amount ($)')
ax7.set_title('Revenue & Profit by Payment Method')
ax7.legend()
ax7.grid(axis='x', alpha=0.3)

# 8. Monthly Profit Trend
ax8 = plt.subplot(3, 3, 8)
df_clean['Order_Month'] = df_clean['Order_Date'].dt.month
monthly_profit = df_clean.groupby('Order_Month')['Profit'].sum()
monthly_profit.plot(kind='line', marker='o', linewidth=2, markersize=8, ax=ax8, color='purple')
ax8.set_xlabel('Month')
ax8.set_ylabel('Total Profit ($)')
ax8.set_title('Monthly Profit Trend')
ax8.set_xticks(range(1, 13))
ax8.grid(alpha=0.3)
ax8.fill_between(monthly_profit.index, monthly_profit.values, alpha=0.3)

# 9. Sales Rep Performance
ax9 = plt.subplot(3, 3, 9)
rep_perf = df_clean.groupby('Sales_Rep').agg({
    'Revenue': 'sum',
    'Profit': 'sum',
    'Order_ID': 'count'
}).sort_values('Profit', ascending=True)
reps = rep_perf.index
x = range(len(reps))
width = 0.35
bars5 = ax9.barh(x, rep_perf['Revenue'], width, label='Revenue', color='skyblue')
bars6 = ax9.barh([i + width for i in x], rep_perf['Profit'], width, label='Profit', color='lightcoral')
ax9.set_yticks([i + width/2 for i in x])
ax9.set_yticklabels(reps)
ax9.set_xlabel('Amount ($)')
ax9.set_title('Sales Rep Performance')
ax9.legend()
ax9.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()

# Additional detailed visualizations
fig2 = plt.figure(figsize=(16, 8))

# Correlation Heatmap
ax10 = plt.subplot(1, 2, 1)
numeric_cols = ['Quantity', 'Unit_Price', 'Discount', 'Shipping_Cost', 
                'Customer_Rating', 'Profit', 'Revenue', 'Profit_Margin', 'Shipping_Delay']
correlation = df_clean[numeric_cols].corr()
mask = np.triu(np.ones_like(correlation, dtype=bool))
sns.heatmap(correlation, mask=mask, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, fmt='.2f', ax=ax10)
ax10.set_title('Correlation Heatmap of Numerical Variables')

# Pie Chart - Order Status Distribution
ax11 = plt.subplot(1, 2, 2)
status_counts = df_clean['Order_Status'].value_counts()
colors = plt.cm.Set3(range(len(status_counts)))
explode = [0.05 if status == 'Returned' else 0 for status in status_counts.index]
wedges, texts, autotexts = ax11.pie(status_counts.values, labels=status_counts.index, 
                                     autopct='%1.1f%%', colors=colors, startangle=90,
                                     explode=explode)
ax11.set_title('Order Status Distribution')

plt.tight_layout()
plt.show()

# Summary dashboard - Country Analysis
fig3, axes = plt.subplots(1, 2, figsize=(14, 6))

# Top Countries by Profit
ax12 = axes[0]
country_profit = df_clean.groupby('Country')['Profit'].sum().nlargest(8)
bars7 = ax12.bar(range(len(country_profit)), country_profit.values, color='teal')
ax12.set_xticks(range(len(country_profit)))
ax12.set_xticklabels(country_profit.index, rotation=45, ha='right')
ax12.set_ylabel('Total Profit ($)')
ax12.set_title('Top 8 Countries by Profit')
for bar, value in zip(bars7, country_profit.values):
    ax12.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
             f'${value:,.0f}', ha='center', va='bottom', fontweight='bold')
ax12.grid(axis='y', alpha=0.3)

# Warehouse Performance
ax13 = axes[1]
warehouse_data = df_clean.groupby('Warehouse').agg({
    'Profit': 'sum',
    'Revenue': 'sum',
    'Order_ID': 'count'
}).sort_values('Profit', ascending=False)
x = range(len(warehouse_data))
width = 0.35
bars8 = ax13.bar(x, warehouse_data['Profit'], width, label='Profit', color='lightgreen')
bars9 = ax13.bar([i + width for i in x], warehouse_data['Revenue'], width, label='Revenue', color='skyblue')
ax13.set_xticks([i + width/2 for i in x])
ax13.set_xticklabels(warehouse_data.index)
ax13.set_ylabel('Amount ($)')
ax13.set_title('Warehouse Performance')
ax13.legend()
ax13.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# Print summary statistics
print("\n" + "="*80)
print("DATA CLEANING SUMMARY")
print("="*80)
print(f"Original rows: {len(df)}")
print(f"Cleaned rows: {len(df_clean)}")
print(f"Duplicates removed: {len(df) - len(df_clean)}")
print("\nKEY METRICS:")
print(f"Total Revenue: ${df_clean['Revenue'].sum():,.2f}")
print(f"Total Profit: ${df_clean['Profit'].sum():,.2f}")
print(f"Overall Profit Margin: {(df_clean['Profit'].sum() / df_clean['Revenue'].sum() * 100):.2f}%")+
print(f"Average Customer Rating: {df_clean['Customer_Rating'].mean():.2f}/5")
print(f"Average Shipping Delay: {df_clean['Shipping_Delay'].mean():.1f} days")
print("\nPRODUCT CATEGORY SUMMARY:")
for category in df_clean['Product_Category'].unique():
    cat_data = df_clean[df_clean['Product_Category'] == category]
    print(f"{category}: Profit=${cat_data['Profit'].sum():,.2f}, "
          f"Margin={((cat_data['Profit'].sum() / cat_data['Revenue'].sum()) * 100):.1f}%")
