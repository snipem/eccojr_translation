import json
import shutil
import sys

from read import Text

def read_texts_from_json(file_path):
    texts = []
    with open(file_path, "r") as file:
        data = json.load(file)
        for item in data:
            text = Text(nr=item['nr'], end_offset=item['end_offset'], length=item['length'], original_text=item['original_text'], start_offset=item['start_offset'], translated_text=item['translat_text'])
            texts.append(text)
    return texts

# Example usage

def write_string_to_offset(file_path, start_offset, end_offset, string_to_write):
    with open(file_path, "r+b") as file:
        # Move the file pointer to the start_offset
        file.seek(start_offset)

        # # Calculate the maximum number of characters that can be written
        # max_chars = min(end_offset - start_offset, len(string_to_write))
        #
        # # Truncate the string if it exceeds the max_chars
        # string_to_write = string_to_write[:max_chars]

        # Write the string to the file
        file.write(string_to_write.encode('ascii'))

if __name__ == '__main__':

    file_path = "texts.json"
    dst =  "Ecco Jr. (USA, Australia).Hack.md"
    shutil.copy("Ecco Jr. (USA, Australia).Base.md", dst=dst)
    texts = read_texts_from_json(file_path)

    for text in texts:
        if text.translat_text != '':

            if len(text.translat_text) != len(text.original_text):
                print("Size difference in text, exiting: %s" % text)
                sys.exit(1)

            if text.original_text.count("\n") != text.translat_text.count("\n"):
                print("Number of newlines difference in text, exiting: %s" % text)
                sys.exit(1)

            # Replace Umlauts
            umlaut_text = text.translat_text
            umlaut_text = umlaut_text.replace('Ö', '\\')
            umlaut_text = umlaut_text.replace('ö', '\\')
            umlaut_text = umlaut_text.replace('Ä', '@')
            umlaut_text = umlaut_text.replace('ä', '@')
            umlaut_text = umlaut_text.replace('Ü', '^')
            umlaut_text = umlaut_text.replace('ü', '^')

            write_string_to_offset(dst, text.start_offset, text.end_offset, umlaut_text)
