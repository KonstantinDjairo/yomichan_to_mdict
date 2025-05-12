import simdjson
import os
import re
from tqdm import tqdm
from pathlib import Path

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', s)]

def process_entry(entry, output_dir):
    """Process individual entries and save as separate files"""
    try:
        # Extract main word (親字)
        headword = ""
        content = []
        
        # Recursive processing function
        def parse_node(node, depth=0):
            nonlocal headword
            if isinstance(node, simdjson.Object):
                for key in node.keys():
                    value = node[key]
                    if key == "親字":
                        headword = str(value)
                    content.append(f"{'  ' * depth}{key}:")
                    parse_node(value, depth + 1)
            elif isinstance(node, simdjson.Array):
                for idx, item in enumerate(node):
                    content.append(f"{'  ' * depth}[{idx}]:")
                    parse_node(item, depth + 1)
            else:
                content.append(f"{'  ' * depth}{node}")

        parse_node(entry)
        
        if headword:
            # Sanitize filename
            safe_headword = re.sub(r'[\\/*?:"<>|]', "", headword)
            file_path = output_dir / f"{safe_headword}.txt"
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"{headword}\n")
                f.write("<html><body>")
                f.write("</body></html>".join(content))
                f.write("\n</>")
                
            return True
        return False
        
    except Exception as e:
        print(f"Error processing entry: {str(e)}")
        return False

# Config
json_dir = Path("./")
output_dir = Path("./articles")
output_dir.mkdir(exist_ok=True)

# Get and sort files naturally
json_files = sorted(
    [f for f in json_dir.iterdir() 
     if f.name.startswith("term_bank") and f.suffix == ".json"],
    key=lambda x: natural_sort_key(x.name)
)

# Process all files
total_entries = 0
for json_file in tqdm(json_files, desc="Processing JSON files"):
    try:
        parser = simdjson.Parser()
        with open(json_file, "rb") as f:
            doc = parser.parse(f.read())
            entries = doc.as_list() if isinstance(doc, simdjson.Array) else [doc]
            
            for entry in entries:
                if process_entry(entry, output_dir):
                    total_entries += 1
                    
    except Exception as e:
        print(f"Error processing {json_file.name}: {str(e)}")

print(f"\nProcessed {total_entries} entries. Files saved to {output_dir}")
