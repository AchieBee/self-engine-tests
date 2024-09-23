import csv

# Define the expected number of fields
EXPECTED_FIELDS = 8

# Input and output file paths
input_file = 'input.csv'
output_file = 'selftestengine.csv'

# Function to clean and validate rows
def clean_and_validate_row(row):
    # Check if row has the expected number of fields
    if len(row) == EXPECTED_FIELDS:
        return row  # No cleaning needed, valid row

    # Handle rows that have fewer or extra fields due to misplaced commas or multi-line breaks
    # We assume questions and answers might contain commas that need to be fixed
    cleaned_row = []
    temp_field = ""
    for field in row:
        # If a field starts with a quote but doesn't end with one, it's likely split by a comma
        if field.startswith('"') and not field.endswith('"'):
            temp_field = field  # Start combining fields
        elif temp_field:
            temp_field += "," + field  # Append field to the previous part
            if field.endswith('"'):
                cleaned_row.append(temp_field)  # End of the combined field
                temp_field = ""  # Reset temp_field
        else:
            cleaned_row.append(field)

    # If there was an unclosed quoted field, append it
    if temp_field:
        cleaned_row.append(temp_field)

    # If the cleaned row still doesn't have the expected number of fields, we skip it
    if len(cleaned_row) == EXPECTED_FIELDS:
        return cleaned_row
    else:
        return None  # Invalid row

# Open the input CSV and the output CSV
with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write the header
    header = next(reader)  # Assuming the first row is the header
    writer.writerow(header)

    # Process each row in the input file
    for row in reader:
        cleaned_row = clean_and_validate_row(row)
        if cleaned_row:
            writer.writerow(cleaned_row)
        else:
            print(f"Skipping invalid row: {row}")

print("CSV file cleaned and written to", output_file)
