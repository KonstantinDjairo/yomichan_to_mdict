# the json's used yomichan are so broken that we need this lib.
import dirtyjson

def process_json_file(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()

    # Define the start and end delimiters
    start_delim = b'---\n'
    end_delim = b'\n---'

    # Initialize the starting position
    start_pos = 0

    while True:
        # Find the start of the next JSON object
        start_pos = content.find(start_delim, start_pos)
        if start_pos == -1:
            break  # No more JSON objects

        # Move past the start delimiter
        start_pos += len(start_delim)

        # Find the end of the JSON object
        end_pos = content.find(end_delim, start_pos)
        if end_pos == -1:
            break  # No end delimiter found, malformed JSON

        # Extract the JSON string
        json_str = content[start_pos:end_pos].decode('utf-8')

        try:
            # Attempt to parse the JSON string
            data = dirtyjson.loads(json_str)
            print("Successfully parsed JSON:", data)
        except dirtyjson.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

        # needs fixing:
        # Move past the end delimiter
        start_pos = end_pos + len(end_delim)


process_json_file('input.txt')
