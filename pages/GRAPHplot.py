from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

load_dotenv()

openai_api_key = os.environ.get('OPENAI_API_KEY')

def main():
    st.title("Plotting Graph and Generating Reports")
    
    # Load the CSV file
    df = pd.read_csv("permanent.csv")
    
    # Get list of numeric and categorical columns
    numeric_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(include=object).columns
    
    # Numeric column selection
    numeric_column = st.selectbox("Select numeric column:", numeric_cols)
    
    # Calculate statistics for numeric column
    numeric_stats = df[numeric_column].describe()
    
    # Display numeric statistics
    st.subheader("Numeric Column Statistics")
    st.write(numeric_stats)
    
    # Categorical column selection
    categorical_column = st.selectbox("Select categorical column:", categorical_cols)
    
    # Calculate count and percentage for categorical column
    categorical_stats = df[categorical_column].value_counts(normalize=True) * 100
    
    # Display categorical statistics
    st.subheader("Categorical Column Statistics")
    st.write(categorical_stats)
    
    # Correlation plot
    st.subheader("Correlation Plot")
    x_column_options = numeric_cols
    y_column_options = numeric_cols
    x_column = st.selectbox("Select x-axis column:", x_column_options)
    y_column = st.selectbox("Select y-axis column:", y_column_options)
    
    # Calculate correlation coefficient
    correlation_coefficient = df[[x_column, y_column]].corr().iloc[0, 1]
    
    # Plot scatter plot with regression line
    fig, ax = plt.subplots()
    plt.scatter(df[x_column], df[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"Correlation: {correlation_coefficient:.2f}")
    st.pyplot(fig)

if __name__ == "__main__":
    main()