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
    
     for fruit_chosen in ingredients_list:
         ingredients_string += fruit_chosen + ' '

         search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
         st.write('The search value for ', fruit_chosen,' is ', search_on, '.')



         
         st.subheader(fruit_chosen + 'Nutrition Information')
         fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_chosen)
         fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
 
     #st.write(ingredients_string)
 
     my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
     editable_df = st.data_editor(my_dataframe)
     Submitted = st.button('Submit')
 
     if Submitted :

 
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
         
        try:
           og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
           st.success('Your Smoothie is ordered!'+""","""+ Name_on_order , icon="✅")

        except:
           st.write('Something went wrong,')
 
     else :
          st.success('There are no pending orders right now')









