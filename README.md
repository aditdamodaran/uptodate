# uptodate

PLEASE NOTE:
TO RUN THIS CODE:
  1. DOWNLOAD THIS REPOSITORY
  2. INSERT YOUR UCHICAGO CNET ID AND PASSWORD IN "scrape.py"
  3. ADJUST "output_generic_names.txt" TO INCLUDE ONLY THE GENERICS YOU ARE MINING DATA FOR (INCLUDING ALL 480+ WILL TAKE A LONG TIME)
  4. RUN THE COMMAND "python scrape.py" FROM WITHIN YOUR DOWNLOADED REPOSITORY, please pip install any dependencies (i.e. Selenium)

THIS CODE WAS WRITTEN IN A macOS ENVIRONMENT, AND IS MEANT TO BE RUN IN PYTHON 2.7 WITH GOOGLE CHROME.


The Linux OS was used to convert the pdf of Authorized Generics to "ag.txt"

get_generic_names.py converts "ag.txt" into "output_generic_names.txt"

scrape.py uses "output_generic_names.txt" as input to write the authorized generics' chemical names and indications to "requested_data.csv"

Because this was done in increments rather than all at once, the data is actually in "authorized_generics_data.csv" rather than "requested_data.csv"
