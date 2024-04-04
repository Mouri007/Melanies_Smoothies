import streamlit as st
import requests

st.title(":cup_with_straw: Customize Your Smoothie! :cat:")
st.write(
    """
    Choose the fruit you want in your Custom Smoothie!
    """)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of smoothie will be:', name_on_order)

ing_list = st.multiselect('choose your 5 fruit:'
                         , ['apple', 'orange', 'banana', 'strawberry', 'blueberry']
                         , max_selections=5
                         )

if ing_list:
    ing_string = ''

    for fruit_chosen in ing_list:
        ing_string += fruit_chosen + ','

        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
             values ('""" + ing_string + """','"""+ name_on_order+"""')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        st.success('Your Smoothie is Ordered!', icon="✅")
