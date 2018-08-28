# uptodate

The Linux OS was used to convert the pdf of Authorized Generics to "ag.txt"

get_generic_names.py converts "ag.txt" into "output_generic_names.txt"

scrape.py uses "output_generic_names.txt" as input to write the authorized generics' chemical names and indications to "requested_data.csv"

Because this was done in increments rather than all at once, the data is actually in "authorized_generics_data.csv" rather than "requested_data.csv"
