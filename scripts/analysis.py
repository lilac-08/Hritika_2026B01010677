import pandas as pd

# Import Excel dataset
df = pd.read_excel("data/raw/sales_data.xlsx", sheet_name="Sales Data")

# Display first 5 rows
print(df.head())

print(df.columns.tolist())
df.info()
print(df.isnull().sum())

# remove duplicate and clean the text 
df = df.drop_duplicates()
for col in ["Region", "State", "City", "Segment", "Category"]:
    df[col] = df[col].astype(str).str.strip().str.title()

# correct numbers and dates
for col in ["List Price", "Sales"]:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

# Handle missing values
df = df.drop(columns=["Internal Notes"], errors="ignore")
df = df.dropna(subset=["Order Date", "Quantity", "List Price", "Sales"])
for col in ["Order Priority", "Sales Rep ID", "Warehouse Code", "Gift Wrap", "City"]:
    df[col] = df[col].fillna("Unknown")

print("Rows remaining:", len(df))
print(df.dtypes)

#cleaned data
import os
os.makedirs("data/processed",exist_ok=True)
df.to_csv("data/processed/cleaned_sales.csv",index=False)
print("cleaned file saved in output folder!")

# Revenue and key numbers
df["Revenue"] = df["Sales"]

print("Total revenue: ₹", f"{df['Revenue'].sum():,.2f}")
print("Unique orders:", df["Order ID"].nunique())
print("Units sold:", df["Quantity"].sum())

# Region wise revenue
region_sales = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
print(region_sales)

# Top 10 products by revenue
product_revenue = df.groupby("Product Name")["Revenue"].sum().sort_values(ascending=False)
print(product_revenue.head(10))

# Monthly revenue
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("Month")["Revenue"].sum().sort_index()
print("Best month:", monthly_sales.idxmax())

import os
import matplotlib.pyplot as plt

# Chart 1: Region wise revenue
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(region_sales.index, region_sales.values, color="#1f77b4")
ax.set_title("Revenue by Region")
ax.set_ylabel("Revenue (Rs)")
fig.savefig("images/revenue_by_region.png")
plt.show()

# Chart 2: Monthly trend
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(monthly_sales.index, monthly_sales.values, marker="o")
ax.set_title("Monthly Revenue Trend")
ax.set_ylabel("Revenue (Rs)")
ax.tick_params(axis="x", rotation=45)
fig.tight_layout()
fig.savefig("images/monthly_revenue_trend.png")
plt.show()

#chart 3: state wise revenue (top 10)
state_sales= df.groupby("State")["Revenue"].sum().sort_values(ascending=False)
print(state_sales.head(10))

top_sales = state_sales.head(10).sort_values()
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(top_sales.index, top_sales.values, color="#1f77b4")
ax.set_title("Top 10 States by Revenue")
ax.set_xlabel("Revenue (Rs)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"Rs{x/1e5:,.1f}L"))
fig.tight_layout()
fig.savefig("images/state_wise_revenue.png")
plt.show()

# Export
os.makedirs("data/processed/", exist_ok=True)
df.to_csv("data/processed/cleaned_sales.csv", index=False)
region_sales.to_csv("data/processed/revenue_by_region.csv", header=["Revenue"])
monthly_sales.to_csv("data/processed/monthly_revenue.csv", header=["Revenue"])

print("Export complete!")