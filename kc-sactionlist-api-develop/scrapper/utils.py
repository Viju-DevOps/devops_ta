import re


def remove_multiple_delimiters(string, delimiter_string):
    """Function to split a string with multiple delimiters

    Args:
        string: String contains multiple delimiters'
        delimiter_string: list of delimiters

    Returns: returns list of strings in which multiple delimiters are removed

    """
    output_string_list = []
    if string:
        string_list = re.split(delimiter_string, string)
        for string in string_list:
            if string != "":
                output_string_list.append(string.strip())
    return output_string_list
