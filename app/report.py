import json
import csv

json_file_path = 'profile_scraper/scraper_outputs/data.json'
csv_file_path = 'profile_scraper/scraper_outputs/report.csv'


# Step 1: Read the JSON file
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Step 2: Prepare your data (this step is conceptual and depends on your JSON structure)

# Step 3: Write to a CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    
    # Iterate through each item in the JSON data
    for item in data:
        # For each key-value pair in the item, write it as a row
        for key, value in item.items():
            writer.writerow([key, value])
        
        # Write an extra blank row to separate each entry
        writer.writerow([])  # This creates the extra space between entries