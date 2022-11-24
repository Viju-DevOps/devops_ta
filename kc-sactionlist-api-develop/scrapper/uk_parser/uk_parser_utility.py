import requests
from bs4 import BeautifulSoup


def start_uk_web_scraping(uk_url):
    """ Function to scrape sanction list from uk html page

    Args:
        uk_url: URL of the UK page

    Returns: returns web scraped raw data from uk website

    """
    r = requests.get(uk_url)

    soup = BeautifulSoup(r.content, 'html5lib')

    sanction_list = soup.find_all('li')
    data_list = []
    for each in sanction_list:
        details_list = each.contents
        data_dict = {}
        key = ''
        value_list = []
        for data in details_list:
            if data.name is not None:
                key = data.string
            else:
                value_list.append(data)
            if key and value_list:
                data_dict[key] = value_list
                key = None
                value_list = []
        data_list.append(data_dict)
    return data_list


def format_uk_data(uk_scrape_data):
    """ Function to format UK scrape data

    Args:
        uk_scrape_data: Uk scrape data

    Returns: returns formatted list of UK data

    """
    sanction_data_list = []
    for scrape_data in uk_scrape_data:
        sanction_data_dict = {}
        if 'Name 6:' in scrape_data.keys():
            first_name = ''
            last_name = scrape_data['Name 6:'][0].strip()
            if scrape_data['1:'][0].strip() != 'n/a':
                first_name = scrape_data['1:'][0].strip()
            if scrape_data['2:'][0].strip() != 'n/a':
                first_name += ' ' + scrape_data['2:'][0].strip()
            if scrape_data['3:'][0].strip() != 'n/a':
                first_name += ' ' + scrape_data['3:'][0].strip()
            if scrape_data['4:'][0].strip() != 'n/a':
                first_name += ' ' + scrape_data['4:'][0].strip()
            if scrape_data['5:'][0].strip() != 'n/a.':
                first_name += ' ' + scrape_data['5:'][0].strip()
            name = first_name + ' ' + last_name
            sanction_data_dict['name'] = name
            if 'Name (non-Latin script):' in scrape_data.keys():
                sanction_data_dict['original_script'] = scrape_data['Name (non-Latin script):'][0].strip()
            if 'Title:' in scrape_data.keys():
                sanction_data_dict['title'] = __generate_list(scrape_data['Title:'])
            if 'DOB:' in scrape_data.keys():
                sanction_data_dict['dob'] = __generate_list(scrape_data['DOB:'])
            if 'POB:' in scrape_data.keys():
                sanction_data_dict['pob'] = __generate_list(scrape_data['POB:'])
            if 'Address:' in scrape_data.keys():
                sanction_data_dict['address'] = __generate_list(scrape_data['Address:'])
            if 'National Identification Number:' in scrape_data.keys():
                sanction_data_dict['national_identification_no'] = __generate_list(scrape_data
                                                                                   ['National Identification Number:'])
            if 'National Identification Details:' in scrape_data.keys():
                sanction_data_dict['national_identification_details'] = __generate_list\
                    (scrape_data['National Identification Details:'])
            if 'Position:' in scrape_data.keys():
                sanction_data_dict['position'] = __generate_list(scrape_data['Position:'])
            if 'Good quality a.k.a:' in scrape_data.keys():
                sanction_data_dict['alias_name_good_quality'] = __generate_list(scrape_data['Good quality a.k.a:'])
            if 'a.k.a:' in scrape_data.keys():
                sanction_data_dict['alias_name_low_quality'] = __generate_list(scrape_data['a.k.a:'])
            if 'Other Information:' in scrape_data.keys():
                sanction_data_dict['other_information'] = __generate_list(scrape_data['Other Information:'])
            if 'Listed on:' in scrape_data.keys():
                sanction_data_dict['listed_on'] = scrape_data['Listed on:'][0].strip()
            if 'Last Updated:' in scrape_data.keys():
                sanction_data_dict['updated_on'] = scrape_data['Last Updated:'][0].strip()
            sanction_data_dict['data_source'] = 'UK'
            sanction_data_list.append(sanction_data_dict)
    return sanction_data_list


def __generate_list(data):
    """Function to generate list from given data and remove unwanted characters

    Args:
        data: Data to be transformed

    Returns: returns the data as a list

    """
    final_data_list = []
    for data_string in data:
        data_string = data_string.replace('\xa0', '').strip()
        data_string = data_string.replace('.', '')
        final_data_list.append(data_string)
    return final_data_list



