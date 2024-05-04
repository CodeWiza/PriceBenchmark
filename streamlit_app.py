import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_elements import elements, mui, html

# Streamlit theme with Purple and White (adjust colors to your preference)
st.set_page_config(page_title="Competitor Price Analysis", layout="wide")

with st.sidebar:
  st.header("Configuration")

# Upload CSV function
def upload_csv():
  uploaded_file = st.sidebar.file_uploader("Upload CSV File", type="csv")
  if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    return df
  else:
    return None

# Read uploaded CSV files
df = upload_csv()

# Sidebar options (assuming data has these columns)
if df is not None:
  # Supplier Name dropdown
  selected_supplier = st.sidebar.selectbox("Supplier Name", df["Supplier Name"].unique())

  # Filter the DataFrame based on the selected supplier
  supplier_df = df[df["Supplier Name"] == selected_supplier]

  # Country dropdown (filtered based on selected supplier)
  selected_country = st.sidebar.selectbox("Country", supplier_df["Country"].unique())

  # Product Name dropdown (filtered based on selected supplier and country)
  supplier_country_df = supplier_df[supplier_df["Country"] == selected_country]
  selected_product = st.sidebar.selectbox("Product Name", supplier_country_df["Product Name"].unique())

  # Price filter
  price_filter = st.sidebar.slider('Unit Price (Less Than)', 0, 10000)

  # Convert "Unit Price" column to numeric
  df["Unit Price"] = pd.to_numeric(df["Unit Price"], errors="coerce")

  # Filter the DataFrame based on selected values
  filtered_df = df[
    (df["Supplier Name"] == selected_supplier)
    & (df["Country"] == selected_country)
    & (df["Product Name"] == selected_product)
    & (df["Unit Price"] <= price_filter)
  ]

  def load_data(path: r"C:\Users\devan\Downloads\From Base\Price Benchmark_Quotation_1.xlsx"):
    data = pd.read_excel(path)
    return data

  df4 = load_data("./Price Benchmark_Quotation_1.xlsx")
  df6 = load_data("./Price_benchmark 1.xlsx")

  with st.expander("Data Preview 1"):
    st.dataframe(df4)

  with st.expander("Data Preview 2"):
    st.dataframe(df6)

  # Calculate statistics for Price_benchmark 1 sheet (assuming "Price" column)
  if "Unit Price" in filtered_df.columns:
    price_stats = filtered_df["Unit Price"]
    highest_price = price_stats.max()
    median_price = price_stats.median()
    lowest_price = price_stats.min()

  with st.expander("Highlights"):
    # Columns for displaying statistics
    col1, col2, col3 = st.columns(3)
    col1.metric("Highest Price", highest_price)
    col2.metric("Median Price", f"{median_price}")
    col3.metric("Lowest Price", f"{lowest_price}")

  # Plot the first bar graph
  fig1 = px.bar(df4, x="Supplier Name", y="Unit Price", color="Product name", barmode="group", text_auto=True, title="All Products Price")
    
  # Get selected product price from Price Benchmark_Quotation1 sheet (assuming "My Price" column)
  selected_product_data = filtered_df[(filtered_df["Product Name"] == selected_product)]

  if not selected_product_data.empty:
    selected_product_price = selected_product_data["Unit Price"].values[0]
  else:
    selected_product_price = 0  # or any other default value you prefer

  #Prepare data for second bar chart
  data = [selected_product_price, lowest_price]
  labels = ["Your Price", "Lowest Competitor Price"]

  # Plot the second bar chart
  fig2 = px.bar(x=labels, y=data, color=labels, title="Price Comparison")

  with elements("dashboard"):
    # You can create a draggable and resizable dashboard using
    # any element available in Streamlit Elements.
    from streamlit_elements import dashboard

    # First, build a default layout for every element you want to include in your dashboard

    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        dashboard.Item("first_item", 0, 0, 2, 2),
        dashboard.Item("second_item", 2, 0, 2, 2),
        ]

    # Next, create a dashboard layout using the 'with' syntax. It takes the layout
    # as first parameter, plus additional properties you can find in the GitHub links below.

    # If you want to retrieve updated layout values as the user move or resize dashboard items,
    # you can pass a callback to the onLayoutChange event parameter.

    def handle_layout_change(updated_layout):
        # You can save the layout in a file, or do anything you want with it.
        # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
        print(updated_layout)

    with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
        mui.Paper(fig1, key="first_item")
        mui.Paper(fig2, key="second_item")