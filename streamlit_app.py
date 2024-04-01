# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import streamlit as st

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cat:")
st.write(
    """
    Choose the fruit you want in your Custom Smoothie!
    """)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ing_list = st.multiselect('choose your 5 fruit:'
                         , my_dataframe
                         , max_selections=5
                                    )
if ing_list:

    ing_string = ''

    for fruit_chossen in ing_list:
        ing_string += fruit_chossen + ', '
    #st.write(ing_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ing_string + """','"""+ name_on_order+"""')"""

    st.write(my_insert_stmt)
    
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothis is Ordered!', icon = "✅")



   
