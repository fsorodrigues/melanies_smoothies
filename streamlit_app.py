# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your Smoothie")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options")
my_column = my_dataframe.select(col('FRUIT_NAME'))

# st.dataframe(data=my_dataframe, use_container_width=True)
name_on_order = st.text_input('Name on smoothie', '')
st.write('The name on your Smoothie will be: ', name_on_order)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_column,
    max_selections = 5
)


if ingredients_list and len(ingredients_list):
    ingredients_string = ""
    for f in ingredients_list:
        ingredients_string += f + ' '

    my_insert_stmt = """
        insert into smoothies.public.orders(
            ingredients, 
            name_on_order
        )
        values ('""" + ingredients_string + """', '""" + name_on_order +"""')
    """

    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(
            f'Your Smoothie is ordered, {name_on_order}!', 
            icon="✅"
        )

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fv_df = st.dataframe(
    data=fruityvice_response.json(),
    use_container_width=True
)