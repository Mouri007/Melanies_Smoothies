# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import streamlit as st
import requests
import pandas

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cat:")
st.write(
    """
    Choose the fruit you want in your Custom Smoothie!
    """)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('SEARCH_ON'))
pd_df=my_dataframe.to_pandas()

ing_list = st.multiselect('choose your 5 fruit:'
                         , my_dataframe
                         , max_selections=5
                                    )
if ing_list:

    ing_string = ''

    for fruit_chossen in ing_list:
        ing_string += fruit_chossen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chossen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chossen,' is ', search_on, '.')

        st.subheader(fruit_chossen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ing_string + """','"""+ name_on_order+"""')"""

    st.write(my_insert_stmt)
    
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothis is Ordered!', icon = "✅")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
