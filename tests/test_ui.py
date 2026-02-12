import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def test_automind_load():
    # Setup Chrome options for the VM environment (Headless is mandatory for Jenkins)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 1. Navigate to your local AutoMind app [cite: 211]
        driver.get("http://localhost")
        
        # 2. Wait for Streamlit's frontend to render [cite: 221]
        time.sleep(5) 

        # 3. Assertion: Verify the app title exists in the page source [cite: 225, 226]
        assert "AutoMind" in driver.page_source
        print("UI Test Passed: AutoMind dashboard is accessible.")
        
    finally:
        # 4. Close the browser session [cite: 226]
        driver.quit()