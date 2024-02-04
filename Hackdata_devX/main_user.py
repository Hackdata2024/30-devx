import streamlit as st
from streamlit_option_menu import option_menu
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from openai import OpenAI
from geopy.geocoders import Nominatim
import numpy as np
import requests
import pandas as pd  # Import Pandas
import geocoder
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # Run in headless mode


def get_address(lat, long):
    g = geocoder.osm([lat, long], method='reverse')
    return g.json

# Example usage:


def get_current_location():
    try:
        # Send a request to the ipinfo.io API to get the current location
        response = requests.get('https://ipinfo.io')
        data = response.json()

        # Extract latitude and longitude
        loc = data.get('loc', 'Unknown').split(',')
        latitude, longitude = loc[0], loc[1]

        return latitude, longitude

    except Exception as e:
        st.error(f"Error getting current location: {e}")
        return None, None


client = OpenAI(api_key="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")
def openAPI(user_input):

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Work as a legal assistant. I will give you the problem statement in the next prompt. First, just in case its an emergency, give the local police contact details according to the kind of the problem. Give it in the following format - ' In case of an emergency, please contact your local police station using the following number under Section PCR: 112'.  Then, provide under which section\sections of the Indian Penal Code the issue could fall under. After this, provide a roadmap with roughly 4-6 detailed steps as to how the user should proceed with their legal issue. Do not include anything about this not constituting legal advice and dont include anything like ' remember its crucial to consult a lawyer' or anything like that after the roadmap steps please also mention under which category the incident falls. I will give the problem statement in the next prompt so respond then"},
        {"role": "user", "content": f"{user_input}"}])

    res = response.choices[0].message.content
    return res

def user():
        st.subheader("Solve your Legal Issue")
        st.write("Provide a brief description of your legal issue and we'll give you a roadmap to follow")

        example_text = "Eg: I was involved in a road accident and want to proceed with filing an application to charge the perpetrator for damages to my car"
        law_text = st.text_area("Input your law problem", placeholder=example_text, key='roadmap')
        submit_button = st.button('Submit')
        st.write(len(law_text), 'characters')

        if law_text or submit_button:
            st.session_state['law_text'] = law_text
            with st.spinner('Generating roadmap...'):
                st.markdown("#### Basic roadmap to solve your legal issue:\n")
                section=openAPI(law_text)
                st.write(section)
            
            st.markdown('###### For more detailed analysis use the analysis tool')
            

        
            st.markdown("###### Law firm website for you:")
            st.link_button("Lawyer 1 website:", url='https://thelawsuits.in/')

        st.write("---")
        st.file_uploader("Upload your Legal Documents", accept_multiple_files=True)
        st.write("---")
        latitude, longitude = get_current_location()
        user_address=get_address(lat=latitude*1,long=longitude*1).get('address')
        st.write("Your Current Location: Latitude ",latitude," Longitude ",longitude)
        def near_police_station():
            driver = webdriver.Chrome(options=options)
            driver.get("https://www.google.com/search?q=police+station+near")
            driver.implicitly_wait(1)
            
            text_area = driver.find_element(by=By.ID,value="APjFqb")
            text_area.click()
            text_area.send_keys(user_address)
            
            search = driver.find_element(by=By.CLASS_NAME,value="Tg7LZd")
            search.click()
            driver.implicitly_wait(2)
            
            link = driver.current_url
            driver.quit()
            st.markdown(f"[Nearby Police Stations ]({link})")
        st.button("NEAR POLICE STATION",on_click=near_police_station)  
         
        if latitude is not None and longitude is not None:
            st.write(f"Your current location: Latitude {latitude}, Longitude {longitude}")
            st.write(F"ADDRESS: {user_address}")

        # Display map with a marker for the user's location
        st.markdown('''
| Department | Phone Number |
| ---- | ---- |
| PCR | 112 (24X7) (Toll Free) |
| Eyes and Ears | 14547 (Toll Free) |
| Women in distress | 1091 |
| Special Cell (North-Eastern States) | 1093 |
| Missing Persons | 1094, 23241210 |
| Traffic | 1095, 25844444 |
| Vigilance (Anti Corruption Helpline ) | 1064 |
| For uploading Audio and Video Clips | 9910641064 |
| Railways | 1512 |
| Senior Citizen | 1291 |
| Cyber Complaints | 1930 |
''')
        driver = webdriver.Chrome(options=options)
        driver.get(f"https://www.google.com/search?q=helpline+numbers+for+{user_address}")
        driver.implicitly_wait(1)
        
        text_area = driver.find_element(by=By.ID,value="APjFqb")
        text_area.click()
        text_area.send_keys(user_address)
        
        search = driver.find_element(by=By.CLASS_NAME,value="Tg7LZd")
        search.click()
        driver.implicitly_wait(2)
        link=driver.current_url
        result_text=requests.get(link)
        soup=BeautifulSoup(result_text.content,"html.parser")
        helpline_links=soup.find_all("a",limit=5)
        st.write("Helpline links")
        j=1
        for i in helpline_links:
            if"https"in i['href'] :
                st.markdown(f'''- [Helpline link {j}]({i['href'][i['href'].find("https"):]})''')
                j+=1
            
        data = pd.DataFrame({
            'lat': [float(latitude)],
            'lon': [float(longitude)]
        })

        # Display map with a marker for the user's location
        st.map(data, zoom=13)


