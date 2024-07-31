
# Import libraries  
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import warnings 
import squarify
warnings.filterwarnings('ignore')


# Load the Dataset
df = pd.read_csv('retail_sales_dataset.csv')


# Data Exploration 
df.shape
df.columns
df.info()
df.describe()


# Most of our customers are around 42 years old, while our top 25% are younger, averaging 29 years old. 
# Typically, customers order about 3 products, with the most being 4. 
# Our best customers spend around 180 on average, but some go up to 500. 
# Overall, the average order totals about 456, with the highest hitting 2000.


df.nunique()
df.isnull().sum()
df.head()
df.tail()


# Data Visualisation 

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Create a figure and set of subplots
fig, axes = plt.subplots(2, 1, figsize=(12, 12))

# Plot Monthly Sales Trend
monthly_sales = df.resample('M', on='Date')['Total Amount'].sum()
axes[0].plot(monthly_sales.index, monthly_sales.values, marker='o')
axes[0].set_title('Monthly Revenue', fontsize=16)
axes[0].set_xlabel('Month', fontsize=14)
axes[0].set_ylabel('Total Sales', fontsize=14)
axes[0].grid(True)
axes[0].set_xticks(monthly_sales.index)
axes[0].set_xticklabels([month.strftime('%b %Y') for month in monthly_sales.index], rotation=45)

# Plot Monthly Sales Trend by Product Category
monthly_category_sales = df.groupby([df['Date'].dt.to_period('M'), 'Product Category'])['Total Amount'].sum().reset_index()
pivot_table = monthly_category_sales.pivot(index='Date', columns='Product Category', values='Total Amount').fillna(0)

for category in pivot_table.columns:
    axes[1].plot(pivot_table.index.to_timestamp(), pivot_table[category], marker='o', label=category)

axes[1].set_title('Monthly Revenue by Product Category', fontsize=16)
axes[1].set_xlabel('Month', fontsize=14)
axes[1].set_ylabel('Total Sales Amount', fontsize=14)
axes[1].grid(True)
axes[1].legend(title='Product Category')
axes[1].set_xticks(pivot_table.index.to_timestamp())
axes[1].set_xticklabels([date.strftime('%b %Y') for date in pivot_table.index.to_timestamp()], rotation=45)

# Adjust layout
plt.tight_layout()
plt.show()


# The monthly revenue was pretty balanced throughout the year, except for May 2023. 
# Looking at the first visual, May 2023 had the highest revenue of the year. 
# The second visual shows that Electronics were behind the spike. 
# It'd be worth digging into what caused that jump in May 2023.


#Total Amount vs Unit Price vs Quantity by Product Category
# Create a figure and set of subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Scatter plot for Total Amount vs Quantity
sns.scatterplot(data=df, x='Quantity', y='Total Amount', hue='Product Category', ax=axes[0])
axes[0].set_title('Total Amount vs Quantity', fontsize=16)
axes[0].set_xlabel('Quantity', fontsize=14)
axes[0].set_ylabel('Total Amount', fontsize=14)
axes[0].grid(True)
axes[0].legend(title='Product Category', bbox_to_anchor=(1.05, 1), loc='upper left')

# Scatter plot for Total Amount vs Price per Unit
sns.scatterplot(data=df, x='Price per Unit', y='Total Amount', hue='Product Category', ax=axes[1])
axes[1].set_title('Total Amount vs Price per Unit', fontsize=16)
axes[1].set_xlabel('Price per Unit', fontsize=14)
axes[1].set_ylabel('Total Amount', fontsize=14)
axes[1].grid(True)
axes[1].legend(title='Product Category', bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout
plt.tight_layout()
plt.show()




#Number of Transactions per Month
# Parse the Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Extract month and year from the Date column
df['YearMonth'] = df['Date'].dt.to_period('M')

# Group by YearMonth and Gender columns and count the number of transactions
transactions_by_gender = df.groupby(['YearMonth', 'Gender']).size().unstack(fill_value=0)

# Group by YearMonth and count the number of transactions
transactions_per_month = df.groupby('YearMonth').size()

# Create a figure and set of subplots
fig, axes = plt.subplots(2, 1, figsize=(12, 12))

# Plot the number of transactions per month
axes[0].plot(transactions_per_month.index.astype(str), transactions_per_month, marker='o')
axes[0].set_title('Number of Transactions per Month', fontsize=16)
axes[0].set_xlabel('Month', fontsize=14)
axes[0].set_ylabel('Number of Transactions', fontsize=14)
axes[0].grid(True)
axes[0].tick_params(axis='x', rotation=45)

# Plot the number of transactions by gender
for gender in transactions_by_gender.columns:
    axes[1].plot(transactions_by_gender.index.astype(str), transactions_by_gender[gender], label=gender, marker='o')

axes[1].set_title('Number of Transactions per Month by Gender', fontsize=16)
axes[1].set_xlabel('Month', fontsize=14)
axes[1].set_ylabel('Number of Transactions', fontsize=14)
axes[1].legend(title='Gender')
axes[1].grid(True)
axes[1].tick_params(axis='x', rotation=45)

# Adjust layout
plt.tight_layout()
plt.show()

# The number of transactions was pretty steady each month. 
# The dip from January to March 2023 might be because of the New Year and people cutting back after spending a lot on Christmas gifts and over the holidays.
# Interestingly, there’s not a huge difference in the number of transactions between males and females. 
# However, it’s clear that men have placed a lot of orders for Electronics in May 2023.




#Age Group Distribution 
# Define age bins and labels
age_bins = [18, 25, 35, 45, 55, 65]
age_labels = ['18-24', '25-34', '35-44', '45-54', '55-64']
df['Age Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

# Create a figure and set of subplots
fig, axes = plt.subplots(2, 1, figsize=(12, 12))

# Plot Age Group Distribution as a bar chart with a darker blue shade
age_distribution = df['Age Group'].value_counts().sort_index()
axes[0].bar(age_distribution.index, age_distribution.values, color='#003366')  
axes[0].set_title('Age Group Distribution', fontsize=16)
axes[0].set_xlabel('Age Group', fontsize=14)
axes[0].set_ylabel('Count', fontsize=14)
axes[0].grid(True)


# Plot Product Category Purchased by Age Group
sns.barplot(x='Age Group', y='Quantity', hue='Product Category', data=df, ax=axes[1])
axes[1].set_title('Product Category Purchased by Age Group', fontsize=16)
axes[1].set_xlabel('Age Group', fontsize=14)
axes[1].set_ylabel('Quantity Purchased', fontsize=14)
axes[1].grid(True)

# Adjust layout
plt.tight_layout()
plt.show()


# Our customer base predominantly consists of individuals aged 35 to 64, 
# indicating that they are more established and likely to have a higher income, 
# as our products are positioned in the premium segment. 
# Beauty products are especially popular among customers aged 18 to 34, while clothing and electronics are more frequently purchased by those in the 35 to 64 age range.






