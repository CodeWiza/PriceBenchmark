import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_elements import elements, mui, html
import plotly.graph_objects as go
from pathlib import Path
import base64

st.set_page_config(page_title="Price Benchmark Analysis",page_icon=":bar_chart:", layout="wide")

st.sidebar.image("https://raw.githubusercontent.com/CodeWiza/PriceBenchmarking-Dashboard/main/logo.png", use_column_width=True)
st.sidebar.header("Filters")

# Upload Files
def upload_csv_myproducts():
  uploaded_file = st.file_uploader("Upload Current Product Pricing", type="xlsx")
  if uploaded_file is not None:
    df1 = pd.read_excel(uploaded_file)
    return df1
  else:
    return None
def upload_csv_competitors():
  uploaded_file = st.file_uploader("Upload Market Pricing", type="xlsx")
  if uploaded_file is not None:
    df2 = pd.read_excel(uploaded_file)
    return df2
  else:
    return None

# ---- MAINPAGE ----
st.title("Price Benchmark Analysis")

# Read uploaded Excel files
with st.expander("Upload Data", expanded= True): 
  df_self = upload_csv_myproducts()
  df_comp = upload_csv_competitors()

with st.expander("Graphs", expanded= True):
  if df_self is not None and df_comp is not None:

    #Displaying uploaded Excel files in a dropdown
    #with st.expander("View Uploaded data"): 
    #  st.write(df_self)
    #  st.write(df_comp)
      
    # ALL SELECTIONS FOR SELF QUOTATION

    # Self ProductName dropdown
    self_product_selected = st.sidebar.multiselect("Product Name", df_self["Product Name"].unique())

    # Convert the list of selected product names to a pandas Series
    self_product_selected = pd.Series(self_product_selected)

    # Filter the dataframe based on selected product names
    self_products = df_self[df_self["Product Name"].isin(self_product_selected)]

    # Self SupplierName dropdown
    self_supplier_selected = st.sidebar.multiselect("Supplier Name", df_self["Supplier Name"].unique(), default=df_self["Supplier Name"].unique())

    # Convert the list of selected supplier names to a pandas Series
    self_supplier_selected = pd.Series(self_supplier_selected)

    # Filter the DataFrame based on the selected supplier
    self_supplier = self_products[self_products["Supplier Name"].isin(self_supplier_selected)]

    # Self Country dropdown
    self_country_selected = st.sidebar.multiselect("Country", df_self["Country"].unique(), default=df_self["Country"].unique())

    # Convert the list of selected country names to a pandas Series
    self_country_selected = pd.Series(self_country_selected)

    # Filter out data based on selected country
    self_country = self_supplier[self_supplier["Country"].isin(self_country_selected)]

    # Filter the dataframe based on selected product names
    filtered_df = self_country

    # Filter the competitor data based on selected product names
    comp_data = df_comp[df_comp["Product Name"].isin(self_product_selected)]

    

    # Merge the filtered data from both sources
    merged_data = pd.merge(filtered_df, comp_data, on=["Product Name"], how="inner")


    # Calculate the difference in unit prices
    merged_data["Price Difference"] = merged_data["Unit Price_y"] - merged_data["Unit Price_x"]

    grouped_data = merged_data.groupby("Product Name")

    self_product_selected = merged_data["Product Name"].unique().tolist()

    # Assuming you have the merged_data DataFrame
    num_tabs = len(self_product_selected)  # Determine the number of columns based on the selected products

    # Check if self_product_selected is not empty
    if self_product_selected:
        x = num_tabs  # Number of tabs
        variable_names = st.tabs(self_product_selected)

        for i, tab_name in enumerate(variable_names):
            with tab_name:
                product = self_product_selected[i]
                product_data = merged_data[merged_data["Product Name"] == product]
                product_data_copy = merged_data[merged_data["Product Name"] == product].iloc[0]  # Get the data for the current product
                # with st.popover(f"{product}",use_container_width= True):
                col1, col2, col3 = st.columns(3)
                # My Price
                my_price = product_data_copy["Unit Price_x"]
                col1.metric("My Price", f"${my_price:.2f}", "")
                # Highest Price
                highest_price = max(product_data["Unit Price_y"])
                col2.metric("Highest Market Price", f"${highest_price:.2f}", "")
                # Lowest Price
                lowest_price = min(product_data["Unit Price_y"])
                col3.metric("Lowest Market Price", f"${lowest_price:.2f}", "")

                if not product_data.empty:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(name="Curent Product Pricing", x=[product], y=[product_data["Unit Price_x"].values[0]]))
                    for supplier, group in product_data.groupby("Supplier Name_y"):
                        fig.add_trace(go.Bar(name=supplier, x=[product], y=group["Unit Price_y"].values))
                    fig.update_layout(
                        title=f"Unit Price Comparison for {product}",
                        barmode="group",
                        xaxis_title="Product",
                        yaxis_title="Unit Price"
                    )
                    st.plotly_chart(fig)
                else:
                    st.write(f"No data available for product: {product}")
    else:
        st.write("")
try:
  with st.expander("INSIGHTS"):
    #st.write(filtered_df)
    #st.write(comp_data)
    st.write(merged_data)
except NameError:
    st.warning("")


#Insights button
#'''result1 = st.button("Insights", key = i)
# #             if result1:
#               description_string = str(product_data_copy["More Info about the supplier"])
#              for segment in description_string.split(", "):
#                  st.write(segment)
#            else:
#             st.write("")'''