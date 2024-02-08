import streamlit as st
import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv("permanent.csv")

# Get list of numeric and categorical columns
numeric_cols = df.select_dtypes(include=np.number).columns
categorical_cols = df.select_dtypes(include=object).columns

# Calculate statistics for numeric columns
numeric_stats = df[numeric_cols].describe()

# Calculate count and percentage for categorical columns
categorical_stats = pd.DataFrame()
for col in categorical_cols:
    count = df[col].value_counts()
    percentage = count / count.sum() * 100
    categorical_stats[col] = count.astype(str) + " (" + percentage.round(2).astype(str) + "%)"

# Display the report using Streamlit
st.title("Data Summary Report")
st.header("Numeric Columns")
st.write(numeric_stats)

st.header("Categorical Columns")
st.write(categorical_stats)