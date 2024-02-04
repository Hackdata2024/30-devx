from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import json
from collections.abc import Mapping
import streamlit as st
import math
import mysql.connector
import pandas as pd  # Import Pandas
from geopy.geocoders import Nominatim
import numpy as np
from openai import OpenAI
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # Run in headless mode


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


# Streamlit app
def Scraped_data():
    user_input=st.text_input("Enter the accident")
    # Connect to MySQL
    
    def scrape():
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that specializes in Indian law. You understand legal terminology and can provide relevant sections of Indian law when given a description of an incident. You communicate by providing only the section numbers, separated by commas and start your response with the section numbers. Give the output only in the following format: Section <Section Number>: <Section Title>. Don't print anything else, and only print the title in the section title, not the description"},
                {"role": "user", "content": f"Please provide the sections of Indian law that would be applicable to this incident: '{user_input}'"},
            ]
        )

        res = response.choices[0].message.content

        sections = res.splitlines()
        responses=[]
        for i in sections: 
            driver = webdriver.Chrome(options=options)
            driver.get("https://www.google.com/search?q=indian+law&sca_esv=351bde09f24e60ac&ei=jDS7Zd-iEs2F4-EP3ZeyuA8&ved=0ahUKEwjfmMe0vImEAxXNwjgGHd2LDPcQ4dUDCBA&oq=indian+law&gs_lp=Egxnd3Mtd2l6LXNlcnAiCmluZGlhbiBsYXcyCxAAGIAEGIoFGJECMgsQABiABBiKBRiRAjILEAAYgAQYsQMYgwEyCxAAGIAEGLEDGIMBMgUQABiABDIREC4YgAQYsQMYgwEYxwEY0QMyDhAAGIAEGIoFGLEDGIMBMgUQABiABDIFEAAYgAQyCxAAGIAEGLEDGIMBSP96UABYz3VwAngBkAEAmAHvBKAB7wSqAQM1LTG4AQPIAQD4AQGoAhTCAiAQABiABBiKBRjlAhjlAhjqAhi0AhiKAxi3AxjUA9gBAcICHRAAGIAEGIoFGOUCGOUCGOoCGLQCGIoDGLcD2AEBwgIWEAAYAxiPARjlAhjqAhi0AhiMA9gBAsICGBAAGAMYjwEY5QIY6gIYtAIYChiMA9gBAsICFhAuGAMYjwEY5QIY6gIYtAIYjAPYAQLiAwQYACBBugYECAEYB7oGBggCEAEYCg&sclient=gws-wiz-serp&uact=5")
            
            title = driver.title
            
            driver.implicitly_wait(1)
            
            text_area = driver.find_element(by=By.ID,value="APjFqb")
            text_area.click()
            text_area.send_keys(f"Latest cases caused under {i} ")
            search=driver.find_element(by=By.CLASS_NAME,value="Tg7LZd")
            search.click()
            driver.implicitly_wait(3.5)
            
            element = driver.find_element(by=By.CLASS_NAME,value="yuRUbf")
            txt=element.text
            link=driver.current_url
            response=requests.get(link)
            html_code=response.text
            soup=BeautifulSoup(f"""{html_code}""",features="lxml")
            arr=soup.find_all("div",class_="Gx5Zad fP1Qef xpd EtOod pkphOe",limit=2)
            i=1
            
            for item in arr:
                response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={ "type": "json_object" },
                messages=[
                {"role": "system", "content": "You are a legal assistant who has all the knowledge of all the laws and gives output in JSON only with title,url,description ."},
                {"role": "user", "content": f'''display in json format'{item}'   '''}
                ] 
                )
                responses.append(response.choices[0].message.content)   
            driver.quit()  # Moved outside of the loop
        
        with open('data.json', 'w') as f:
         json.dump(responses, f)
    st.button("Submit",on_click=scrape) 
    # Load the JSON file and display the data
    with open("data.json") as f:
        data = json.load(f)

    # Display the data using st.write
    for i in range(len(data)):
        dict = json.loads(data[i])
        title = dict.get("title", "No title available")
        url = dict.get("url", "No URL available")
        description = dict.get("description", "No description available")
        st.subheader(f"{i+1}.")
        st.write(f"Title: {title}")
        st.write(f"URL: {url}")
        st.write(f"Description: {description}")
        st.divider()
            

        
       
       # Get current location
        # Get current location
