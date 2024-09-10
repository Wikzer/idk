#Packages
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import zscore

@st.cache_data  # Cache the function to enhance performance
def load_data():
    # Define the file path
    file_path = 'https://github.com/Cheide20/assignments/raw/main/DatabankWide.xlsx'
    df = pd.read_excel(file_path)

    return df
df = load_data()

# Set the app title and sidebar header
st.title("Welcome to our first app, used to run analysis on the data")
st.sidebar.header("Filters 📊")

# Introduction
st.markdown("""
Welcome, the following app will help you run an analysis on the data based on your specified guidelines.
""")


with st.expander("📊 **Objective**"):
    st.markdown("""
This dashboard shows the filtered data.
""")

#The following is a subset that limits the dataset. Is extended a little bit from our initial "opgave kan ikke lige huske oversættelsen"
columns_to_include = [
    "Country name", "Country code", "Year", "Adult populaiton", "Region", "Income group",
    "Account (% age 15+)", "Financial institution account (% age 15+)",
    "First financial institution account ever was opened to receive a wage payment or money from the government (% age 15+)",
    "First financial institution account ever was opened to receive a wage payment (% age 15+)",
    "First financial institution ever account was opened to receive money from the government (% age 15+)",
    "Owns a credit card (% age 15+)", "Used a credit card (% age 15+)", 
    "Used a credit card: in-store (% age 15+)", "Used a credit card: in-store (% who used a credit card, age 15+)",
    "Paid off all credit card balances in full by their due date (% age 15+)", 
    "Paid off all credit card balances in full by their due date (% who used a credit card, age 15+)", 
    "Owns a debit card (% age 15+)", "Used a debit card (% age 15+)", 
    "Used a debit card in-store (% age 15+)", "Used a debit card: in-store (% who used a debit card, age 15+)", 
    "Owns a debit or credit card (% age 15+)", "Used a debit or credit card (% age 15+)", 
    "Uses a debit or credit card: in-store (% age 15+)", 
    "Used a debit or credit card: in-store (% who use a credit or debit card, age 15+)"
]

#Det subsettede data
df_subset = df[columns_to_include]

#Kode til valg af kolonner
selected_columns = st.sidebar.multiselect("Select Columns to Display", columns_to_include, default=columns_to_include)

if selected_columns:
    filtered_df = df_subset[selected_columns]
    cleaned_data = filtered_df.dropna(subset=['Region', 'Income group', 'Adult populaiton'])
    data_na = cleaned_data.fillna({
    'First financial institution account ever was opened to receive a wage payment or money from the government (% age 15+)': cleaned_data['First financial institution account ever was opened to receive a wage payment or money from the government (% age 15+)'].mean(),
    'Used a credit card: in-store (% age 15+)': cleaned_data['Used a credit card: in-store (% age 15+)'].median(),
    'Paid off all credit card balances in full by their due date (% age 15+)': cleaned_data['Paid off all credit card balances in full by their due date (% age 15+)'].mean(),
    'Owns a credit card (% age 15+)': cleaned_data['Owns a credit card (% age 15+)'].fillna(0),
    'Adult populaiton': cleaned_data['Adult populaiton'].mean(),  # Assuming you want to fill the mean for population
    'Income group': cleaned_data['Income group'].ffill(),  # Using forward fill for categorical data like income group
    'Financial institution account (% age 15+)': cleaned_data['Financial institution account (% age 15+)'].median(),
    'Used a debit card in-store (% age 15+)': cleaned_data['Used a debit card in-store (% age 15+)'].median(),
    'Owns a debit card (% age 15+)': cleaned_data['Owns a debit card (% age 15+)'].fillna(0),
    'Used a debit card (% age 15+)': cleaned_data['Used a debit card (% age 15+)'].median(),
    'Uses a debit or credit card: in-store (% age 15+)': cleaned_data['Uses a debit or credit card: in-store (% age 15+)'].median()})
    st.dataframe(data_na)


#Kode til at identificere hvilken form for statistisk information man vil have printet
st.title("Dataset Summary")
st.write("### Full Dataset Summary")
st.write(data_na.describe())  # Static summary statistics

#Bruges til at vise hvilke kolonner der skal fremvises
st.write("### Choose Columns and Statistics to Display")

stat_options = st.multiselect(
    "Select Statistics to Display", 
    ["Mean", "Median", "Standard Deviation (std)", "Minimum (min)", "Maximum (max)", "Quartiles"]
)

selected_columns = st.multiselect("Select Columns", cleaned_data.columns.tolist())

def display_column_statistics(data_na, selected_columns, stat_options):
    if not selected_columns:
        st.warning("Please select at least one column.")
        return
    
for col in selected_columns:
        st.subheader(f"Statistics for {col}")
        for stat in stat_options:
            if stat == "Mean":
                st.write(f"**Mean**: {data_na[col].mean()}")
            elif stat == "Median":
                st.write(f"**Median**: {data_na[col].median()}")
            elif stat == "Standard Deviation (std)":
                st.write(f"**Standard Deviation**: {data_na[col].std()}")
            elif stat == "Minimum (min)":
                st.write(f"**Minimum**: {data_na[col].min()}")
            elif stat == "Maximum (max)":
                st.write(f"**Maximum**: {data_na[col].max()}")
            elif stat == "Quartiles":
                st.write(f"**Quartiles**: {data_na[col].quantile([0.25, 0.5, 0.75])}")
        st.markdown("---")


# Kalder på funktionen for hvad der skal fremvises
if selected_columns and stat_options:
    display_column_statistics(cleaned_data, selected_columns, stat_options)


# Laver et flexibelt boxplot
st.title("Flexible Boxplot")

def create_boxplot(data, x_col, y_col):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x=x_col, y=y_col)
    plt.title(f'Box Plot of {y_col} by {x_col}')
    st.pyplot(plt)

x_axis = st.selectbox("Select X-axis (Categorical)", data_na.columns.tolist(), index=0)
y_axis = st.selectbox("Select Y-axis (Numerical)", data_na.columns.tolist(), index=1)

if x_axis and y_axis:
    create_boxplot(data_na, x_axis, y_axis)

# laver print af sampling fordeling med og uden outliers
#--------------------------------------------------------------------------------------
st.write("### Calculations of outliers effect")

# Checkboxes for toggling plots
show_clean = st.checkbox("Show graph with outliers only", value=True)
show_out = st.checkbox("Show graph without outliers ", value=True)

# Create the plot
fig, ax = plt.subplots()

if show_clean:
    ax.plot(data_na['x'], data_na['XXX'], marker='o', linestyle='-', color='blue', label='Clean Plot')

if show_out:
    ax.plot(data_na['x'], data_na['XXX'], marker='o', linestyle='-', color='green', label='Outlier Plot')

ax.legend()
st.pyplot(fig)

# Display the data used for plotting
st.write("Data used for the plots:")
st.dataframe(data_na)





# knap til print af variance, range, std. afvigelse, kurtosis og skewness osv.

st.write("### Calculation of dataset properties")

stat_options_prop = st.multiselect(
    "Select Properties to Display", 
    ["Variance", "Range", "Kurtosis", "Skewness"]
)

selected_columns_prop = st.multiselect("Select Columns to display", cleaned_data.columns.tolist())

def display_column_statistics(data_na, selected_columns_prop, stat_options_prop):
    if not selected_columns_prop:
        st.warning("Please select at least one column.")
        return
    
for col in selected_columns_prop:
        st.subheader(f"Properties for {col}")
        for stat in stat_options_prop:
            if stat == "Variance":
                st.write(f"**Variance**: {data_na[col].var()}")
            elif stat == "Range":
                st.write(f"**Range**: {data_na[col].max()- data_na[col].min()}")
            elif stat == "Kurtosis":
                st.write(f"**Kurtosis**: {data_na[col].kurtosis()}")
            elif stat == "Skewness":
                st.write(f"**Skewness**: {data_na[col].skew()}")
        st.markdown("---")

# Kalder på funktionen for hvad der skal fremvises
if selected_columns_prop and stat_options_prop:
    display_column_statistics(data_na, selected_columns_prop, stat_options_prop)


# correlation matrix

# test
