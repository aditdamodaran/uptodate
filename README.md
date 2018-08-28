# uptodate

To ru nthis code:
  1. Download this repository
  2. Insert your UChicago CNET ID and PASSWORD in "scrape.py"
  3. Adjust "output_generic_names.txt" to include only the generics you are mining data for (Including all 480+ will take a long time)
  4. Run the command "python scrape.py" from within your downloaded repository, please pip install any dependencies (i.e. Selenium)
  5. The output will be written to "requested_data.csv"

THIS CODE WAS WRITTEN IN A macOS ENVIRONMENT, AND IS MEANT TO BE RUN IN PYTHON 2.7 WITH GOOGLE CHROME.

The Linux OS was used to convert the pdf of Authorized Generics to "ag.txt"

get_generic_names.py converts "ag.txt" into "output_generic_names.txt"

scrape.py uses "output_generic_names.txt" as input to write the authorized generics' chemical names and indications to "requested_data.csv"

Because this was done in increments rather than all at once, the data is actually in "authorized_generics_data.csv" rather than "requested_data.csv"
