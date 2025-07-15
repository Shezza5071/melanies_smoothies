import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col, lit

# UI title and instructions
st.title("Customize Your Smoothie! 🥤")
st.markdown("Choose the fruits you want in your custom Smoothie!")

# Input for smoothie name
name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your smoothie will be:", name_on_order)

# Get fruit list from Snowflake table
cnx = st.connection("snowflake")
session = cnx.session()
fruit_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
fruit_list = fruit_df['FRUIT_NAME'].tolist()

# Let user select up to 5 ingredients
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_list, max_selections=5)

# Build and submit the order
if ingredients_list and name_on_order:
    ingredients_string = ', '.join(ingredients_list)
    st.write("Ingredients selected:", ingredients_string)

    if st.button('Submit Order'):
        session.table("smoothies.public.orders").insert([lit(ingredients_string), lit(name_on_order)])
        st.success("✅ Your Smoothie is ordered!")

# External API request to get fruit info
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

if smoothiefroot_response.status_code == 200:
    fruit_data = smoothiefroot_response.json()
    df = pd.DataFrame([fruit_data]) if isinstance(fruit_data, dict) else pd.DataFrame(fruit_data)
    st.dataframe(df, use_container_width=True)
else:
    st.error("Failed to fetch data from Smoothiefroot API.")
