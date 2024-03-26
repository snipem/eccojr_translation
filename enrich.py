import json
import sys

from write import read_texts_from_json

def expand_string(string, length):
    """
    Expand the given string left and right equally with spaces to match the given length.

    Parameters:
        string (str): The input string to be expanded.
        length (int): The desired length of the expanded string.

    Returns:
        str: The expanded string with spaces added to left and right.
    """
    # Calculate the number of spaces needed to expand the string
    spaces_needed = length - len(string)

    # Calculate the number of spaces to add on each side
    spaces_left = spaces_needed // 2
    spaces_right = spaces_needed - spaces_left

    # Expand the string by adding spaces on both sides
    expanded_string = ' ' * spaces_left + string + ' ' * spaces_right

    return expanded_string

def expand_translat_text_to_match_original_text(translat_text: str, original_text: str) -> str:

    if len(translat_text) == len(original_text):
        return translat_text
    elif len(translat_text) > len(original_text):
        proposal_text = translat_text[0:len(original_text)]
        print("Error: translat_text is longer than original_text: %s > %s = %s" % (translat_text, original_text, proposal_text))
        sys.exit(1)
    else:
        return expand_string(translat_text, len(original_text))

if __name__ == '__main__':

    texts = read_texts_from_json("texts.json")

    with open('strings_de.txt', 'r') as file:
        # Read each line and store them in an array
        lines = file.readlines()

    for i, text in enumerate(texts):

        if i >= len(lines):
            print("%d: Cannot proceed with translation for text: %s. Not enough lines" % (text.nr, text))
            break
        else:
            translat_candidate = lines[i].replace("\n", "")
            if translat_candidate != "":

                # introduce actual newlines
                translat_candidate = translat_candidate.replace("\\n", "\n")

                text.translat_text = expand_translat_text_to_match_original_text(translat_candidate, text.original_text)
                print("%d: Translated %s to %s" % (text.nr, text.original_text, text.translat_text))

    with open('texts.json', 'w') as file:
        json.dump([text.__dict__ for text in texts], file, indent=4)
