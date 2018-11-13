# uptodate

To run this code:
  1. Download this repository
  2. Insert your UChicago CNET ID and PASSWORD in "scrape.py" Edit the path to the location of your chromedriver. (You should download
  chromedriver from here https://sites.google.com/a/chromium.org/chromedriver/) 
  3. Adjust "output_generic_names.txt" to include only the generics you are mining data for (Including all 480+ will take a long time)
  4. Run the command "python scrape.py" from within your downloaded repository, please pip install any dependencies (i.e. Selenium)
  5. The output will be written to "requested_data.csv"

This code was is meant to be run with Python 2 and Google Chrome.


Process:

The Linux OS was used to convert the pdf of Authorized Generics to "ag.txt"

get_generic_names.py converts "ag.txt" into "output_generic_names.txt"

scrape.py uses "output_generic_names.txt" as input to write the authorized generics' chemical names and indications to "requested_data.csv"

Because this was done in increments rather than all at once, the data is actually in "authorized_generics_data.csv" rather than "requested_data.csv"

"singlescrape.py" scrapes the data for a single authorized generic and prints it to the terminal. Used primarily for testing.
