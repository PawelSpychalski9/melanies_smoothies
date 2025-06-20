import streamlit as st
from snowflake.snowpark.functions import col

st.title("Customize Your Smoothie")
st.write("Choose the fruits you want....")

# Połączenie do Snowflake
cnx = st.connection("snowflake")
session = cnx.session

# Wybór owocu (statyczny selectbox)
option = st.selectbox("What fruit", ("Banana", "Strawberries", "Peaches"))
st.write("You selected:", option)

# Pobranie danych z tabeli
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

# Lista dostępnych owoców
ingredients = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Multiselect do wyboru składników
ingredients_list = st.multiselect(
    "Select up to 5 ingredients",
    ingredients,
    max_selections=5
)

# Pole tekstowe na nazwę zamówienia
name_on_order = st.text_input("Name on Order")
st.write(name_on_order)

# Tylko jeśli coś wybrano
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ' '.join(ingredients_list)

    st.write(ingredients_string)

    # Przygotowanie INSERT
    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Przycisk
    if st.button("Submit"):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
