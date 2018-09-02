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

def main():
    # This is the process for getting a chemical name and indication for a drug
    # The process is inside a for-loop that iterates over a list of drugnames
    # which it gets from "output_generics_names.txt"
    generics_names_file = open("output_generics_names.txt", 'r')
    generics_names_data = generics_names_file.read()
    generic_names_list = generics_names_data.splitlines()
    for name in generic_names_list:
        driver.get("https://www-uptodate-com.proxy.uchicago.edu/contents/search")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Search UpToDate'])[1]/following::input[1]").send_keys(name)
        driver.find_element_by_name("searchForm").submit()
        search(name)

    driver.quit()

    # Zip our lists into rows (so we can insert them column-wise into a spreadsheet)
    rows = zip(generic_names_list,list_of_chemical_names, indications_list)

    # Write to a .csv file
    with open("requested_data.csv", "w") as output_file_two:
        writer = csv.writer(output_file_two)
        for row in rows:
            writer.writerow(row)

def search(name):
    try:
        get_chemical_name_by_search_suggestion(name)
        navigate_to_drug_info_page(name)
        get_indication(name)
    except Exception as e:
        try:
            get_chemical_name_by_text_of_first_link(name)
            navigate_to_drug_info_page(name)
            get_indication(name)
        except:
            list_of_chemical_names.append("Couldn't get chemical name.")
            indications_list.append("Couldn't get indication.")
            print("Couldn't get chemical name or indication.\n")

def get_indication(name):
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

def navigate_to_drug_info_page(name):
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

def get_chemical_name_by_text_of_first_link(name):
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

def get_chemical_name_by_search_suggestion(name):
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

# Calling Sequence
main()
