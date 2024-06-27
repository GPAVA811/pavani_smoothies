# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """choose the fruits you want"""
)
 
 
Name_on_order = st.text_input('Name on Smootie')
st.write("The name on your Smothiee will be",Name_on_order)
 
cnx = st.connection("snowflake") 
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the snowpark Dataframe to a Pandas Dtaframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
 
ingredients_list = st.multiselect(
    'choose upto 5 Ingredients:'
    , my_dataframe
    , max_selections = 5
)
 
if ingredients_list:
     ingredients_string = ''
    
     for fruit_choosen in ingredients_list:
         ingredients_string += fruit_choosen + ' '

         search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'search_on'].iloc[0]
         st.write('The search value for ', fruit_choosen,' is ', search_on, '.')



         
         st.subheader(fruit_choosen + 'Nutrition Information')
         fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choosen)
         fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
 
     #st.write(ingredients_string)
 
     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + """','"""+ Name_on_order +"""')"""
     time_to_insert = st.button('Submit Order')
     if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+""","""+ Name_on_order , icon="✅")
     st.write(my_insert_stmt)
     st.stop()








