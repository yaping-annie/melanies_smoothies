# Import python packages
import requests
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Customize Your Somoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be: ", name_on_order)

# Get active Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)


if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    st.write(ingredients_string)

    # SQL insert statement with parameter placeholders
    my_insert_stmt = """
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES (:1, :2)
    """

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        try:
            session.sql(my_insert_stmt, (ingredients_string, name_on_order)).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred: {e}")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width=True)
