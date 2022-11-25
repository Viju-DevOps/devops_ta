import re
import json
import datetime

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


def split_values_and_generate_list(lst):
    """Function to extract individual place from a string
    of comma separated places.

    Args:
        lst: list containing list of multiple places'

    Returns: returns list of strings in which individual places are seperated

    """
    return json.dumps([single_place for places in lst for single_place in places.split(",") if single_place !=""])


def dob_format_converter_uk(dob_string):
    """Function to extract individual dobs from a string
    of number "(0)" seperated dobs.

    Args:
        dob_string: string containing list of multiple dobs'
        

    Returns: returns list of strings in which individual dobs are seperated

    """
    import datetime
    dates=[]
    digits_delimiters_dob= r'[(][0-9]\)'
    converter=remove_multiple_delimiters(dob_string, digits_delimiters_dob)

    for i in converter:
        if "--" in i:
            dates.append(i[-4:])
        elif "/" in i:
            raw_date = datetime.datetime.strptime(i, "%d/%m/%Y")
            s = raw_date.strftime('%Y-%m-%d')
            dates.append(s)
        else:
            dates.append(i)
    
    return json.dumps(dates)


def dob_format_converter_us(date_list):
    """Function to extract individual dobs from a string
    of number "(0)" seperated dobs and containing "circa" and months in letter format.

    Args:
        dob_string: string containing list of multiple dobs'
        

    Returns: returns list of strings in which individual dobs are seperated

    """
    dates=[]
    for dob_string in date_list:
        if "/" in dob_string:
            raw_date = datetime.datetime.strptime(dob_string, "%d/%m/%Y")
            s = raw_date.strftime('%Y-%m-%d')
            dates.append(s)
        elif "circa" in dob_string:
            continue
        elif dob_string.isalpha()==True:
            continue
        elif dob_string[:4].isdigit()==True:
            dates.append(dob_string)
    return dates