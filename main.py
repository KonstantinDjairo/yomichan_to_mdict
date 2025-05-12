# the json's used yomichan are so broken that we need this lib.
import dirtyjson
from tqdm import tqdm

def find_next_start(content, start, delimiter):
    """Find the next valid start position after current block"""
    next_start = content.find(delimiter, start)
    return next_start if next_start != -1 else -1

def count_blocks(content, delimiter):
    return content.count(delimiter)

def process_json_file(file_path, output_path):
    with open(file_path, 'rb') as f:
        content = f.read()

    delimiter = b'--------------------------------------------------\n'
    delim_len = len(delimiter)
    total_blocks = count_blocks(content, delimiter)
    start_pos = 0

    with open(output_path, 'w', encoding='utf-8') as out, tqdm(total=total_blocks, desc="Processing blocks") as pbar:
        while True:
            start_pos = find_next_start(content, start_pos, delimiter)
            if start_pos == -1:
                break

            end_pos = find_next_start(content, start_pos + delim_len, delimiter)
            if end_pos == -1:
                break

            json_bytes = content[start_pos + delim_len:end_pos]
            start_pos = end_pos
            pbar.update(1)

            json_string = json_bytes.decode('utf-8', errors='replace').strip()

            try:
                parsed = dirtyjson.loads(json_string)
                if isinstance(parsed, list) and parsed:
                    out.write("headword: " + str(parsed[0]) + '\n')
                    out.write("content: " + str(parsed) + '\n\n')
            except Exception:
                continue  # silently skip bad blocks

process_json_file('input.txt', 'output.txt')
