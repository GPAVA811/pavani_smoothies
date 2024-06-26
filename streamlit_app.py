# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col
 
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """choose the fruits you want"""
)
 
 
Name_on_order = st.text_input('Name on Smootie')
st.write("The name on your Smothiee will be",Name_on_order)
 
cnx = st.connection("snowflake") 
session = cnx_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
 
ingredients_list = st.multiselect(
    'choose upto 5 Ingredients:'
    , my_dataframe
    , max_selections = 5
)
 
if ingredients_list:
     ingredients_string = ''
     for fruit_choosen in ingredients_list:
         ingredients_string += fruit_choosen + ' '
 
     #st.write(ingredients_string)
 
     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + """','"""+ Name_on_order +"""')"""
     time_to_insert = st.button('Submit Order')
     if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+""","""+ Name_on_order , icon="✅")
     st.write(my_insert_stmt)
     st.stop()