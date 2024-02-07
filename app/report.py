import json
import csv
import os
from app.file_utils import save_to_file, create_directory

def main_report(keyword):

    csv_file_path = save_to_file({keyword}, 'leads_and_messages', 'report.csv')
    json_file_path = save_to_file({keyword}, 'leads_and_messages', 'report.txt')

    try: 
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Write to a CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            
            # Iterate through each item in the JSON data
            for item in data:
                # For each key-value pair in the item, write it as a row
                for key, value in item.items():
                    writer.writerow([key, value])
                
                # Write an extra blank row to separate each entry
                writer.writerow([])  # This creates the extra space between entries
    except Exception as e:
        print(f"Failed to write to the report. Error: {e}")

if __name__ == "__main__":
    base_directory = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    main_report()