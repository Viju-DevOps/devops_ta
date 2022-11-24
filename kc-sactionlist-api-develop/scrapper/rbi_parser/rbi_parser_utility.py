import requests
from bs4 import BeautifulSoup
import time
import re
from utils import remove_multiple_delimiters


def start_rbi_web_scraping(rbi_dynamic_url):
    """ Function to scrape sanction list from RBI dynamic url

    Args:
        rbi_dynamic_url:

    Returns: returns web scraped raw data from rbi website

    """
    r = requests.get(rbi_dynamic_url)

    soup = BeautifulSoup(r.content, 'html5lib')
    data = []

    timeout = time.time() + 10  # 10 secs from now
    while True:
        table = soup.find('table', id='sanctions')
        if table or time.time() > timeout:
            break
    if table:
        table_body = table.find('tbody')

        rows = table_body.find_all('tr', attrs={'class': 'rowtext'})
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
    return data


def get_rbi_data_list(rbi_raw_data):
    """Function to process web scraped raw rbi data

    Args:
        rbi_raw_data: rbi raw data from web scrape

    Returns: return rbi sanctions list

    """
    counter = 0
    sanction_list = []
    digits_delimiters = r'1:|2:|3:|4:'
    alphabet_delimiters = r'a\)|b\)|c\)|d\)|e\)|f\)|g\)'

    for data in rbi_raw_data:
        sanction_data_dict = {}
        # counter = counter+1
        # if counter == 2:
        #     break
        data_details = data[0].split('\xa0')
        name, original_script, title = __fetch_name_original_script_and_title(data_details[1])
        name = remove_multiple_delimiters(name, digits_delimiters)
        name = __modify_name_string_list(name)
        sanction_data_dict['name'] = name
        sanction_data_dict['original_script'] = original_script
        sanction_data_dict['title'] = remove_multiple_delimiters(title, alphabet_delimiters)
        sanction_data_dict['designation'] = __fetch_details(data_details, 'Designation:')
        dob = __fetch_details(data_details, 'DOB:')
        sanction_data_dict['dob'] = remove_multiple_delimiters(dob, alphabet_delimiters)
        pob = __fetch_details(data_details, 'POB:')
        sanction_data_dict['pob'] = remove_multiple_delimiters(pob, alphabet_delimiters)
        good_quality = __fetch_details(data_details, 'Good quality a.k.a.:')
        sanction_data_dict['alias_name_good_quality'] = remove_multiple_delimiters(good_quality, alphabet_delimiters)
        sanction_data_dict['alias_name_low_quality'] = __fetch_details(data_details, 'low quality a.k.a.:')
        nationality = __fetch_details(data_details, 'Nationality:')
        sanction_data_dict['nationality'] = remove_multiple_delimiters(nationality, alphabet_delimiters)
        passport_no = __fetch_details(data_details, 'Passport no:')
        sanction_data_dict['passport_no'] = remove_multiple_delimiters(passport_no, alphabet_delimiters)
        national_identification_no = __fetch_details(data_details, 'National identification no:')
        sanction_data_dict['national_identification_no'] = remove_multiple_delimiters(national_identification_no, alphabet_delimiters)
        address = __fetch_details(data_details, 'Address:')
        sanction_data_dict['address'] = remove_multiple_delimiters(address, alphabet_delimiters)
        sanction_data_dict['listed_on'] = __fetch_details(data_details, 'Listed on:')
        sanction_data_dict['other_information'] = __fetch_details(data_details, 'Other information:')
        sanction_data_dict['data_source'] = "RBI"
        sanction_list.append(sanction_data_dict)
    return sanction_list


def __modify_name_string_list(string_list, separator=" "):
    """Function to modify the name string

    Args:
        separator: Separator between each string
        string_list: List of string as input

    Returns: returns string in which separator is added in between each string

    """
    output_string = separator.join([string.strip() for string in string_list if string.strip() != 'na']).strip()
    return output_string


def __fetch_details(data_details, data_identifier):
    """Function to fetch data value from data details

    Args:
        data_details:
        data_identifier:

    Returns: returns the exact value

    """
    data_value = 'na'
    for data in data_details:
        if data.startswith(data_identifier):
            data_value = data.split(data_identifier)[1].strip()
            data_value = data_value.replace('\n', '')
            data_value = data_value.replace('\t', '')
            data_value = re.sub(' +', ' ', data_value)
            break
    if data_value == 'na':
        return None
    return data_value


def __fetch_name_original_script_and_title(name_string):
    """Function to split Name, Original script and Title from the name string

    Args:
        name_string: string contains Name, Original script and Title

    Returns: returns Name, Original script and Title as separate string

    """
    if 'Name (original script):' in name_string:
        name_details_list = name_string.split('Name (original script):')
        original_script_title = name_details_list[1].split('Title:')
        original_script = original_script_title[0].strip()
        title = original_script_title[1].strip()
    else:
        name_details_list = name_string.split('Title:')
        original_script = None
        title = name_details_list[1].strip()

    name = name_details_list[0].split('Name:')[1].strip()
    if title.strip() == 'na':
        title = None
    return name, original_script, title

