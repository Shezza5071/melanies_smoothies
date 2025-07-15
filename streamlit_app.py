# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session  # This gives you the Snowpark session

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

# Get list of fruit names from the DataFrame
fruit_list = fruit_df['FRUIT_NAME'].tolist()

# Let user select up to 5 ingredients
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_df, max_selections=5)

# Build and submit the order
if ingredients_list and name_on_order:

    # Convert list to space-separated string
    ingredients_string = ', '.join(ingredients_list)

    st.write("Ingredients selected:", ingredients_string)

    # Add submit button
    if st.button('Submit Order'):
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(insert_stmt).collect()
        st.success("✅ Your Smoothie is ordered!")

