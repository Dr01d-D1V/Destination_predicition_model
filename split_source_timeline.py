# --- SCRIPT TO SPLIT TIMELINE DATA BY MONTH ---
import json
import os
 
source_json_file_path = "./source_timeline/Gmaps_Timeline_aaron.json"
formated_files_path = "./split_timelines/"

def split_timeline_by_month(source_json_path, output_directory='.'):
    """
    Reads a Google Maps Timeline JSON file, groups the timeline objects by month and year,
    and saves them into separate JSON files.

    Args:
        source_json_path (str): The file path for the source Google Timeline JSON.
        output_directory (str): The directory where the split JSON files will be saved.
                                Defaults to the current directory.
    """
    print(f"--- Starting to split '{source_json_path}' by month ---")

    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: '{output_directory}'")

    try:
        with open(source_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The source file was not found at '{source_json_path}'")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{source_json_path}'.")
        print("Please check if the file is a valid JSON and not empty/corrupted.")
        return

    # Check for the root 'semanticSegments' key
    semantic_segments = data.get("semanticSegments", [])
    if not semantic_segments or not isinstance(semantic_segments, list):
        print("Error: Could not find a list of 'semanticSegments' in the JSON file.")
        return

    # Dictionary to hold objects grouped by 'YYYY-MM'
    monthly_data = {}
    processed_count = 0
    skipped_count = 0

    for item in semantic_segments:
        timestamp_str = item.get('startTime')

        if timestamp_str:
            # Debugging print statement:
            # print(f"Processing timestamp: '{timestamp_str}'")
            try:
                # Extract YYYY-MM from the timestamp string (e.g., "2018-09-23T05:00:00.000+01:00")
                year_month = timestamp_str[:7] # Extracts "YYYY-MM"
                if year_month not in monthly_data:
                    monthly_data[year_month] = []
                monthly_data[year_month].append(item)
                processed_count += 1
            except (IndexError, TypeError) as e:
                print(f"Warning: Error parsing 'startTime' '{timestamp_str}' for an item. Details: {e}. Skipping item.")
                skipped_count += 1
        else:
            print(f"Warning: Item missing 'startTime' field. Skipping item: {item.keys()}") # Print keys to see structure
            skipped_count += 1

    if not monthly_data:
        print("\n No data was grouped by month. Check the timestamp format in your JSON file.")
        print(f"Total semantic segments processed: {processed_count + skipped_count}")
        print(f"Segments with valid timestamps: {processed_count}")
        print(f"Segments skipped (missing/invalid timestamp): {skipped_count}")
        print("Possible reasons: 'semanticSegments' array was empty, or no 'startTime' was found/parsed correctly in any item.")
        return

    # Write each group to its own JSON file
    for year_month, objects_list in monthly_data.items():
        output_filename = f"timeline_{year_month}.json"
        output_filepath = os.path.join(output_directory, output_filename)
        
        # Structure the output file to be similar to the original Takeout file
        output_data = {"semanticSegments": objects_list}
        
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4)
        
        print(f"Successfully created '{output_filepath}' with {len(objects_list)} objects.")

    print("\n--- Splitting process finished ---")
    print(f"Total semantic segments processed: {processed_count}")
    print(f"Total semantic segments skipped: {skipped_count}")


def main(source_path, output_path):
    """
    This script is to initialize the timeline spliting function
    """
    split_timeline_by_month(source_path, output_path)


if __name__ == "__main__":

    main(source_json_file_path, formated_files_path)