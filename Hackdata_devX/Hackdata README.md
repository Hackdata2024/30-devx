# LegalEase README

## Project Title: LegalEase - A Virtual Law Assistant

### Problem Statement:
Navigating the legal system can be complex and intimidating for common people. Moreover, lawyers often need to conduct extensive research to find precedents and analyze similar cases. This process can be time-consuming and inefficient.

### Proposed Solution:
We propose *LegalEase, a two-pronged solution consisting of a **Virtual Law Assistant* for the public and an *Analysis Tool* for legal professionals.

#### 1. Virtual Law Assistant:
A chatbot-like feature that provides immediate assistance to individuals when they encounter a legal incident. It guides them through a roadmap to justice, offering step-by-step advice tailored to their situation.
#### 2. Analysis Tool for Lawyers:
A powerful tool that conducts comprehensive research on previous cases related to a specific legal section. It provides an analysis of similar cases, aiding lawyers in court proceedings and making their fight for justice more effective.
#### 3. Legal Document Generator
Implement a feature that helps users generate common legal documents such as contracts, wills, or power of attorney based on their specific needs.Provide customizable templates and guide users through the process of filling out the necessary details.
#### 4. Legal Education and Glossary
Include a comprehensive legal glossary to help users understand legal terms and jargon. Integrate educational resources to provide users with basic legal knowledge and empower them to make informed decisions.
### Impact:
LegalEase aims to democratize access to legal information, empower individuals to understand their rights, and equip lawyers with data-driven insights to enhance their legal strategies.

### Technology Stack:
- Natural Language Processing (NLP) for understanding user queries and providing relevant responses.
- Machine Learning (ML) for analyzing past legal cases and predicting outcomes.
- Web Development (Frontend & Backend) for creating a user-friendly interface.

### Future Scope:
- Expansion of the legal database to include international laws and cases.
- Integration with voice assistants for hands-free operation.
- Development of a mobile application for on-the-go legal assistance.
- Can be linked to a social platform made for lawyers so they can connect with each other and share insights and experiences

This project aligns with the hackathon's theme of leveraging technology to solve real-world problems and has the potential to revolutionize the legal industry. Let's make justice more accessible and efficient with LegalEase! 
## Prerequisites
- Python 3
### Python Libraries
```Python
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
import pandas as pd
import geocoder
import json
from collections.abc import Mapping
import math
```
### Environmental Variables
- Search > "Edit Environment Variables"
- In user variable section, click on "New"
- In "Variable Name" enter "OPEN_API_KEY"
- In "Variable Value" enter your OpenAI API key
## How to run?
- Clone the repository from GitHub using `git clone` in an empty folder
- Open the terminal in the folder you just cloned
- Run the following command `streamlit run main_ease.py`

