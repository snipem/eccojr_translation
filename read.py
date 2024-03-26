import json
import pprint

class Text:

    def __init__(self, nr: int, original_text: str, translated_text: str, start_offset: int, end_offset: int, length: int):
        self.nr = nr
        self.start_offset = start_offset
        self.length = length
        self.end_offset = end_offset
        self.translat_text = translated_text
        self.original_text = original_text

    def __repr__(self):
        return f'Text(original_text={self.original_text}, translated_text={self.translat_text}, start_offset={hex(self.start_offset)}, end_offset={hex(self.end_offset)}, length={self.length})'

    def __str__(self):
        return self.__repr__()

def read_ascii_from_offset(filename, offset, end_offset):
    read_strings = []
    i = 0
    with open(filename, 'rb') as file:
        file.seek(offset)  # Move the file pointer to the desired offset
        ascii_chars = ''
        while True:
            char = file.read(1)  # Read one byte at a time
            current_offset = file.tell()

            if char == b'\x00':  # Stop reading if end of file or null byte is encountered
                i+=1
                current_end_offset = current_offset - 2 # because detected before
                read_strings.append(Text(i, ascii_chars, '', current_start_offset, current_end_offset, current_end_offset - current_start_offset))
                ascii_chars = ''
            elif not char or current_offset >= end_offset:
                break
            else:
                if ascii_chars == '':
                    current_start_offset = current_offset-1
                ascii_chars += char.decode('ascii', errors='replace')  # Convert byte to ASCII character


    return read_strings

if __name__ == '__main__':

    filename = 'Ecco Jr. (USA, Australia).Base.md'
    texts = []

    offset_pairs = [
        [0x0008B256, 0x0008B3D9], # Title
        [0x000923A8, 0x00092C6D], # Missions
        [0x000A65D4, 0x000A7C79], # Dolphin facts
        [0x000A6159, 0x000A6214], # Parents Options
        [0x00002D11, 0x00003040], # Credits
    ]

    for offset_pair in offset_pairs:

        offset = offset_pair[0]
        end_offset = offset_pair[1]
        texts += read_ascii_from_offset(filename, offset, end_offset)

    pprint.pprint(texts)

    # Serialize the array to JSON format
    json_data = json.dumps([text.__dict__ for text in texts], indent=4)

    # Write the JSON data to a file
    file_path = "texts.json"
    with open(file_path, "w") as file:
        file.write(json_data)

    file_path = "strings_en.txt"
    with open(file_path, "w") as file:
        for text in texts:
            file.write(text.original_text.replace('\n', '\\n'))
            file.write("\n")
