import os
import lxml
import csv
# SELENIUM
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium Driver with Google Chrome
chromedriver = r"/Users/(name)/Desktop/PATH/TO/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chromedriver)

# LOGIN
driver.get("https://www-uptodate-com.proxy.uchicago.edu/contents/search")
driver.find_element_by_id("username").clear()

# INSERT YOUR CNET ID IN PLACE OF [USERNAME], REMOVE BRACKETS
driver.find_element_by_id("username").send_keys("[USERNAME]")
driver.find_element_by_id("password").clear()
# INSERT YOUR CNET PASSWORD IN PLACE OF [PASSWORD], REMOVE BRACKETS
driver.find_element_by_id("password").send_keys("[PASSWORD]")
driver.find_element_by_name("_eventId_proceed").click()

# The two fields we are getting data for
list_of_chemical_names = []
indications_list = []

# Enter the name of the drug to get information for
name = "Accolate"

def search():
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Search UpToDate'])[1]/following::input[1]").send_keys(name)
    driver.find_element_by_name("searchForm").submit()

    try:
        get_chemical_name_by_search_suggestion()
        navigate_to_drug_info_page()
        get_indication()
    except Exception as e:
        try:
            get_chemical_name_by_text_of_first_link()
            navigate_to_drug_info_page()
            get_indication()
        except:
            list_of_chemical_names.append("Couldn't get chemical name.")
            indications_list.append("Couldn't get indication.")
            print("Couldn't get chemical name or indication.\n")

    driver.quit()

    # Print
    print(list_of_chemical_names)
    print(indications_list)

def get_indication():
    # Wait for the database to load the drug's information
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="topicContent"]')))

    # Two separate CSS selectors help to grab the indication
    # An assumption is made that the indication is formatted into either of
    # these two sections. This is true ~85% of the time, but is not always
    # the case. Hence data-cleaning is suggested.

    # Read indication from Dosing Adult section
    dosing_adult_one = driver.find_elements_by_class_name("doa")
    dosing_adult_two = driver.find_elements_by_class_name("doa")

    # The first section is any text one indent after "Dosing: Adult"
    dosing_adult_body_one = dosing_adult_one[0].find_elements_by_css_selector("p[style*='text-indent:-2em;margin-left:2em;'] b:nth-of-type(1)")
    # The second section is bold text within the Dosing Adult title
    dosing_adult_body_two = dosing_adult_two[0].find_elements_by_css_selector("b:nth-of-type(1)")

    # Get the drug information page as an HTML string
    html_doc_as_string = driver.page_source

    # A list that to append indications too (incase there are multiple)
    combined_strings_list = []

    # Simply grab the indications based on our assumption that they are
    # in the sections outlined above. Append the raw HTML into the list.
    # Filter out any "Notes", which tend to contain extraneous info
    # not relevant to the indications
    two_string = dosing_adult_body_two[0].get_attribute('innerHTML')
    if(two_string != "Note:"):
        two_string = two_string.encode('utf-8')
        combined_strings_list.append(two_string)

    for i in range(0,len(dosing_adult_body_one)):
        one_string = dosing_adult_body_one[i].get_attribute('innerHTML')
        if(one_string != "Note:"):
            one_string = one_string.encode('utf-8')
            combined_strings_list.append(one_string)

    # remove duplicates
    combined_strings_list = list(set(combined_strings_list))
    # correctly sort the list by reversing it
    combined_strings_list = combined_strings_list[::-1]
    # combine the list of strings (indications) into a single string
    combined_string_indication = ' '.join(combined_strings_list)
    # append to the list of indications
    indications_list.append(combined_string_indication)
    print(combined_string_indication+"\n")


def navigate_to_drug_info_page():
    try:
        # First try to get the indication using the ": Drug information" link
        try:
            driver.find_element_by_partial_link_text(': Drug information').click()
        except:
            pass
        # Otherwise try using the "Systemic link"
        try:
            driver.find_element_by_partial_link_text('Systemic').click()
        except:
            pass
    except Exception as e:
        # print the error message
        print(e)
        # append a notification to our list so we know to get it manually
        indications_list.append("Couldn't get indication.")
        print("Couldn't get indication.\n")



def get_chemical_name_by_text_of_first_link():
    # Wait for the database to load the drug's information
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-results-container"]')))

    # Get the HTML code
    js_code = "return document.getElementById('appContainer').innerHTML"
    html_doc_as_string = driver.execute_script(js_code)

    # Find the text of the first link
    chemical_name_finder = ": Drug information"
    index_of_name = html_doc_as_string.find(chemical_name_finder) - 1

    chemical_name = ""

    # Read in the first link character by character
    # into our empty string
    while html_doc_as_string[index_of_name] != '>':
        character = html_doc_as_string[index_of_name]
        chemical_name += character
        index_of_name-=1

    # Reverse string since it was read backwards
    chemical_name = chemical_name[::-1]
    chemical_name = chemical_name.encode('utf-8')
    # Append to our list
    list_of_chemical_names.append(chemical_name)
    print(name + ": " + chemical_name)


def get_chemical_name_by_search_suggestion():
    # Wait for the database to output HTML that can be scraped
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="alias-suggestion"]')))

    # Get the HTML code
    js_code = "return document.getElementById('appContainer').innerHTML"
    html_doc_as_string = driver.execute_script(js_code)

    # Find the chemical name based on search suggestion
    chemical_name_finder = "suggestion.candidates"
    index_of_name = html_doc_as_string.find(chemical_name_finder) + len("suggestion.candidates[0].value'>")

    # Read the chemical name into a list
    chemical_name = ""

    while html_doc_as_string[index_of_name] != '<':
        character = html_doc_as_string[index_of_name]
        chemical_name += character
        index_of_name+=1

    chemical_name = chemical_name.encode('utf-8')
    list_of_chemical_names.append(chemical_name)

    # Print the chemical name for reference
    print(name + ": " + chemical_name)

search()
