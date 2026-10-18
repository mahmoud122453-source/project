import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load CSV file
df = pd.read_csv("sales.csv")

print("✅ Data loaded successfully\n")

# Step 2: Preview the data
print("📌 First 5 rows of data:")
print(df.head(), "\n")

print("📌 Data Info:")
print(df.info(), "\n")

# Step 3: Basic Summary
print("📊 --- Basic Summary ---")
print("Total Sales:", df["Sales"].sum())
print("Average Sales:", df["Sales"].mean())
print("Maximum Sale:", df["Sales"].max())
print("Minimum Sale:", df["Sales"].min())
print()

# Step 4: Groupby Analysis
if "Product" in df.columns:
    sales_by_product = df.groupby("Product")["Sales"].sum()
    print("Sales by Product:\n", sales_by_product, "\n")

if "Region" in df.columns:
    sales_by_region = df.groupby("Region")["Sales"].sum()
    print("Sales by Region:\n", sales_by_region, "\n")

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    monthly_sales = df.groupby(df["Date"].dt.to_period("M"))["Sales"].sum()
    print("Monthly Sales:\n", monthly_sales, "\n")

# Step 5: Visualizations
if "Product" in df.columns:
    sales_by_product.plot(kind="bar", figsize=(6,4), title="Sales by Product",
                          ylabel="Total Sales", xlabel="Product", color="skyblue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if "Region" in df.columns:
    sales_by_region.plot(kind="pie", autopct='%1.1f%%', figsize=(6,6), title="Sales by Region")
    plt.ylabel("")
    plt.show()

if "Date" in df.columns:
    monthly_sales.plot(kind="line", marker="o", figsize=(8,4), title="Monthly Sales Trend", ylabel="Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
