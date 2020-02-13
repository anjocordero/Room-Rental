import csv

'''
Errors:
- null characters
- non-numeric characters found in floats
- commas found inside text strings
- non-standard comma character
'''

'''
CREATE TABLE {table} (\
        0  id INT PRIMARY KEY,\
        1  name TEXT,\
        2  host_id INT,\
        3  host_name TEXT,\
        4  neighbourhood_group TEXT,\
        5  neighbourhood TEXT,\
        6  latitude FLOAT,\
        7  longitude FLOAT,\
        8  room_type TEXT,\
        9  price INT,\
        10 minimum_nights INT,\
        11 number_of_reviews INT,\
        12 last_review DATE,\
        13 reviews_per_month FLOAT(2),\
        14 calculated_host_listings_count INT,\
        15 availability_365 INT\
    )

Unique data types:
    - Int (only numeric)
    - Text (all characters allowed)
    - Float (numeric with a single decimal point)
    - Date (YYYY-MM-DD, numeric only)
'''

def clean(dataFile):
    try:
        with open(dataFile, 'r', newline='') as f:

            # Eliminate null characters and strange commas
            reader = csv.reader(line.replace("\0", "").replace("，", ",") for line in f)

            with open(dataFile.replace(".csv", "") + "_CLEAN.csv", 'w', newline='') as fileToWrite:
                writer = csv.writer(fileToWrite)
                header = True
                for row in reader:
                    if not header:
                        # Remove non-numeric symbols from numeric fields
                        # 0 2 (6) (7) 9 10 11 12* (13) 14
                        indices = [0, 2, 6, 7, 9, 10, 11, 12, 13, 14]
                        for index in indices:
                            row[index] = ''.join(c for c in row[index] if c in '1234567890.-')

                    header = False
                    writer.writerow(row)
    except FileNotFoundError as err:
        print(err)
        exit(1)