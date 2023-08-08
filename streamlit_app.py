import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Parents New Healthy Dinner")
 
streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 and Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach and Rocket Smoothie')
streamlit.text('🥑🍞 Hard Boiled Free Ranged Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
 # take json version of response and normalize it
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 # output it the screen as a table
 return fruityvice_normalized

# New header section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 if not fruit_choice:
  streamlit.error("Please select a fruit to get information")
 else:
  back_from_function = get_fruityvice_data(fruit_choice)
  streamlit.dataframe(back_from_function)
  
except URLEror as e:
 streamlit.stop()

streamlit.text("The fruit load list contains:")
#Snowflake-related functions
def get_fruit_list():
 with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from fruit_load_list")
      return my_cur.fetchall()

# Add a button to load the fruit
streamlit.header("View Our Fruit List - Add Your Favourites!")
if streamlit.button('Get Fruit List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_fruit_list()
 my_cnx.close()
 streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
 with my_cnx.cursor() as my_cur:
  my_cur.execute("INSERT INTO FRUIT_LOAD_LIST values ('"+ new_fruit +"')")
  return "Thanks for adding" + new_fruit
  
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
 snowflake.connector.connect(**streamlit.secrets["snowflake"])
 back_from_function = insert_row_snowflake(add_my_fruit)
 streamlit.text(back_from_function)

