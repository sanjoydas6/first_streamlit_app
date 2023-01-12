import streamlit
import pandas
import requests
#import response
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
# Display the table on the page.
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit")
streamlit.text(fruityvice_response)

streamlit.text(fruityvice_response.json())
# Parses the Json

# Parses in Pandas

#create a repeatable code block (called function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit" + this_fruit_choice)
  streamlit.text('Thanks for Adding the Fruit')
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
#New Section to display fruityvice api response

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  #fruit_choice = "kiwi"
  if not fruit_choice:
    streamlit.error("Please select a fruit to get the information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  

    
#streamlit.write('The user entered ', fruit_choice)

# requirements.txt abc

#streamlit.stop()

#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("select * from fruit_load_list")
#my_data_rows = my_cur.fetchall()
streamlit.header("The fruit list contains:")
#Snowflake related Functions

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
        
#Add a Button to load the Fruit

#if streamlit.button('Get Fruit Load List'):
  #my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  #my_data_rows = get_fruit_load_list()
  #streamlit.dataframe(my_data_rows)
  

    
#Allow End User to add a Fruit to the List

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    #my_cur.execute("insert into fruit_load_list values('from streamlit')")
    my_cur.execute("insert into fruit_load_list values(' "+ add_my_fruit +" ')")
    return "Thanks for adding  " + new_fruit
                       
#streamlit.dataframe(my_data_rows)
#add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit') 
add_my_fruit = streamlit.text_input('View our Fruit List - Add your favorites') 
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
  
streamlit.stop()

#streamlit.write('The user entered ', add_my_fruit)
#my_cur.execute("insert into fruit_load_list values('from streamlit')")


