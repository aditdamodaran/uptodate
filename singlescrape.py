import os
import lxml
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chromedriver = "/Users/aditdamodaran/Desktop/uptodate/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chromedriver)

# LOGIN
driver.get("https://www-uptodate-com.proxy.uchicago.edu/contents/search")
driver.find_element_by_id("username").clear()
driver.find_element_by_id("username").send_keys("USERNAME")
driver.find_element_by_id("password").clear()
driver.find_element_by_id("password").send_keys("PASSWORD")
driver.find_element_by_name("_eventId_proceed").click()


list_of_chemical_names = []
indications_list = []

# SEARCH
driver.get("https://www-uptodate-com.proxy.uchicago.edu/contents/search")
# RENAME ACCOLATE TO NAME
driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Search UpToDate'])[1]/following::input[1]").send_keys("PARAPLATIN")
driver.find_element_by_name("searchForm").submit()

# GET CHEMCIAL NAME
try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="alias-suggestion"]')))

    js_code = "return document.getElementById('appContainer').innerHTML"
    html_doc_as_string = driver.execute_script(js_code)
    chemical_name_finder = "suggestion.candidates"
    index_of_name = html_doc_as_string.find(chemical_name_finder) + len("suggestion.candidates[0].value'>")

    chemical_name = ""

    while html_doc_as_string[index_of_name] != '<':
        character = html_doc_as_string[index_of_name]
        chemical_name += character
        index_of_name+=1

    list_of_chemical_names.append(chemical_name)

    # GET INDICATION
    try:
        try:
            driver.find_element_by_partial_link_text(': Drug information').click()
        except:
            pass
        try:
            driver.find_element_by_partial_link_text('Systemic').click()
        except:
            pass
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="topicContent"]')))
        dosing_adult_one = driver.find_elements_by_class_name("doa")
        dosing_adult_two = driver.find_elements_by_class_name("doa")
        dosing_adult_body_one = dosing_adult_one[0].find_elements_by_css_selector("p[style*='text-indent:-2em;margin-left:2em;'] b:nth-of-type(1)")
        dosing_adult_body_two = dosing_adult_two[0].find_elements_by_css_selector("b:nth-of-type(1)")
        html_doc_as_string = driver.page_source

        combined_strings_list = []

        q_string = dosing_adult_body_two[0].get_attribute('innerHTML')
        if(q_string != "Note:"):
            print(q_string + "q")
            combined_strings_list.append(q_string)

        for i in range(0,len(dosing_adult_body_one)):
            p_string = dosing_adult_body_one[i].get_attribute('innerHTML')
            print(p_string + "p")
            if(p_string != "Note:"):
                combined_strings_list.append(p_string)

        combined_string_indication = ' '.join(combined_strings_list)
        indications_list.append(combined_string_indication)
        print(combined_string_indication)
    except:
        indications_list.append("Couldn't get indication.")
        print("Couldn't get indication.")

    print(chemical_name)

except:
    try:
        print("now we are here")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-results-container"]')))

        js_code = "return document.getElementById('appContainer').innerHTML"
        html_doc_as_string = driver.execute_script(js_code)
        chemical_name_finder = ": Drug information"
        index_of_name = html_doc_as_string.find(chemical_name_finder) - 1

        print(index_of_name)
        print(html_doc_as_string)

        chemical_name = ""

        while html_doc_as_string[index_of_name] != '>':
            character = html_doc_as_string[index_of_name]
            chemical_name += character
            index_of_name-=1

        chemical_name = chemical_name[::-1]
        list_of_chemical_names.append(chemical_name)
        print(chemical_name)
    except:
        list_of_chemical_names.append("Couldn't get chemical name.")
        indications_list.append("Couldn't get indication.")
        print("Couldn't get chemical name or indication.")

driver.quit()
print(list_of_chemical_names)
print(indications_list)
