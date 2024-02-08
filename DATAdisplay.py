import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
import os
import shutil

# Set Thai language support
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_page_config(page_title="Thai Language Support", page_icon=":flag-th:")

# Create Streamlit app
def main():
    # Add a file uploader to the app
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if uploaded_file is not None:
        # Specify the directory path where you want to save the temporary CSV file
        save_directory = "./pages/"

        # Create the directory if it doesn't exist
        os.makedirs(save_directory, exist_ok=True)

        # Create a temporary file
        temp_csv_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False, dir=save_directory)
        temp_csv_filename = temp_csv_file.name

        # Save the uploaded Excel file as a CSV
        df = pd.read_excel(uploaded_file)
        df.to_csv(temp_csv_filename, index=False)

        # Close the temporary file
        temp_csv_file.close()

        # Move the temporary CSV file to a permanent location
        permanent_csv_filename = os.path.join(save_directory, "permanent.csv")
        shutil.move(temp_csv_filename, permanent_csv_filename)

        # Get all column names
        all_columns = df.columns.tolist()

        # Let the user choose a numeric column for max, min, and average
        numeric_column = st.selectbox("Select a numeric column", all_columns, key='numeric')

        try:
            # Read the numeric values from the CSV
            numeric_values = pd.read_csv(permanent_csv_filename, usecols=[numeric_column])[numeric_column]
        except ValueError:
            st.write(f"Unable to convert {numeric_column} column to numeric.")
            return

        if numeric_values.dtype in [float, int]:
            max_value = numeric_values.max()
            min_value = numeric_values.min()
            avg_value = numeric_values.mean()

            st.write("Maximum:", max_value)
            st.write("Minimum:", min_value)
            st.write("Average:", avg_value)

            # Plot line chart with X marking the average
            plt.figure()
            sns.lineplot(data=numeric_values)
            plt.axhline(y=avg_value, color='r', linestyle='--', label='Average')
            plt.xlabel('Index')
            plt.ylabel(numeric_column)
            plt.legend()
            st.pyplot(plt)

        else:
            st.write("Invalid column selection. Please choose a numeric column.")

        # Let the user choose a categorical column for counts and percentages
        categorical_column = st.selectbox("Select a categorical column", all_columns, key='categorical')

        if df[categorical_column].dtype == object:
            # Read the categorical values from the CSV
            counts = pd.read_csv(permanent_csv_filename)[categorical_column].value_counts()
            percentages = pd.read_csv(permanent_csv_filename)[categorical_column].value_counts(normalize=True) * 100

            st.write("Counts:")
            st.dataframe(counts)

            st.write("Percentages:")
            st.dataframe(percentages)

            # Plot pie chart
            plt.figure()
            plt.pie(percentages, labels=percentages.index, autopct='%1.1f%%')
            plt.axis('equal')
            st.pyplot(plt)

        else:
            st.write("Invalid column selection. Please choose a categorical column.")

if __name__ == "__main__":
    main()