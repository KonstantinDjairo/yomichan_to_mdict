import simdjson
import os
from tqdm import tqdm
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', s)]

def process_entry(entry, output_file, depth=0):
    """Recursively process entries with proper array handling"""
    try:
        if isinstance(entry, simdjson.Array):
            # Convert to list first as recommended by simdjson docs
            entry_list = entry.as_list()
            for idx, item in enumerate(entry_list):
                output_file.write(f"{'  ' * depth}[{idx}]:\n")
                process_entry(item, output_file, depth + 1)
        elif isinstance(entry, simdjson.Object):
            # Process object key-value pairs
            for key in entry.keys():
                value = entry.get(key)
                output_file.write(f"{'  ' * depth}{key}:\n")
                process_entry(value, output_file, depth + 1)
        else:
            # Primitive value
            output_file.write(f"{'  ' * depth}{entry}\n")
    except Exception as e:
        output_file.write(f"\nERROR PROCESSING ENTRY: {str(e)}\n")

# Config
json_dir = "./"  # path where your json files are
output_path = "output.txt"

# Get and sort files naturally
json_files = sorted(
    [f for f in os.listdir(json_dir) 
     if f.startswith("term_bank") and f.endswith(".json")],
    key=natural_sort_key
)

with open(output_path, "w", encoding="utf-8") as output_file:
    for fname in tqdm(json_files, desc="Processing Files", unit="file"):
        file_path = os.path.join(json_dir, fname)
        output_file.write(f"\n=== {fname} ===\n\n")
        
        try:
            # Read file as bytes
            with open(file_path, "rb") as f:
                parser = simdjson.Parser()
                doc = parser.parse(f.read())
                
                # Convert root array to list immediately
                if isinstance(doc, simdjson.Array):
                    entries = doc.as_list()
                else:
                    entries = [doc]
                
                for entry in entries:
                    output_file.write("-" * 50 + "\n")
                    process_entry(entry, output_file)
                    output_file.write("-" * 50 + "\n\n")
                    
        except Exception as e:
            output_file.write(f"\nFILE PROCESSING ERROR: {str(e)}\n")
            continue

print(f"\nComplete! Output saved to {output_path}")
