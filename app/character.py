def get_characters_in_range(file_path, start_position, end_position):
    with open(file_path, 'r') as f:
        text = f.read()
        if end_position <= len(text):
            return text[start_position:end_position]
        else:
            return None

file_path = "job_table.json"  # Replace this with the name of your JSON file
start_position = 89380  # Replace this with the starting position
end_position = 89405  # Replace this with the ending position

characters = get_characters_in_range(file_path, start_position, end_position)

if characters is None:
    print(f"No characters found between positions {start_position} and {end_position}.")
else:
    print(f"Characters between positions {start_position} and {end_position}: '{characters}'")
