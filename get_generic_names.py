import csv

# Open the file "ag.txt" which contains
# a list of Authorized Generics
with open('ag.txt', 'r') as input_file:
    data = csv.reader(input_file)
    generics_names = []

    # Break into rows
    for elements in data:
        counter = 0
        # Break into columns
        for row in elements:
            row = row.split()
            # Break into Generics (first column)
            for generics_info in row:
                # The item number indicates
                # the row (index) of the generic
                # whose info we are gathering
                item_number = row[0]
                if generics_info is None:
                    continue
                else:
                    try:
                        # Ensure we are counting unique rows
                        if(isinstance(int(item_number), int)):
                            if (item_number > counter):
                                counter = item_number
                                # Generic Name
                                proprietary_name = row[1]
                                proprietary_name_part_two = row[2]
                                # If the Generic Name is followed by a Number (i.e. STALEVO 100)
                                try:
                                    if(isinstance(int(proprietary_name_part_two), int)):
                                        generics_names.append(row[1]+" "+row[2])
                                # Find the Generic Name based on its formmat (Uppercase)
                                except:
                                    if proprietary_name_part_two.isupper():
                                        generics_names.append(row[1]+" "+row[2])
                                    else:
                                        generics_names.append(row[1])
                                # Optional Debugging Print Statements
                                # print("counter %d", counter)
                                # print("item number %d", item_number)
                            else:
                                continue
                    except:
                        continue

# Sort the generics alphabetically
generics_names_list = (sorted(set(generics_names)))

# Write Authorized Generics List to a text file
output_file = open('output_generics_names.txt', 'w')
for item in generics_names_list:
  output_file.write("%s\n" % item)
