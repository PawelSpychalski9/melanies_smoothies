# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
st.title("Customize Your Smoothie")
st.write(
"Choose the fruits you want...."
)


cnx = st.connection("snowflake")

option = st.selectbox(
    "What fruit",
    ("Bannana", "Strowberries", "Peaches"),
)

st.write("You selected:", option)


#session = get_active_session()
session = cnx.session

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Select up to 5 ingredients",
    my_dataframe
    , max_selections=5
)

#st.write(my_insert_stmt)
name_on_order = st.text_input("Name on Order")
st.write(name_on_order)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

my_insert_stmt = f"""insert into SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order)
values ('{ingredients_string}', '{name_on_order}')"""

#st.write(my_insert_stmt)
























time_to_insert = st.button("Subbimit")

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
