from rbi_parser.get_dynamic_url import get_rbi_dynamic_url
from rbi_parser.rbi_parser_utility import start_rbi_web_scraping, get_rbi_data_list


def start_rbi_parsing(rbi_url_list):
    """ Function to parse sanction list from RBI urls

    Args:
        rbi_url: List of RBI sanction list urls

    Returns: return the sanctioned list from rbi page

    """
    
    rbi_sanction_list = []

    for url in rbi_url_list:
        dynamic_url = get_rbi_dynamic_url(url)
        if dynamic_url:
            scrape_data = start_rbi_web_scraping(dynamic_url)
            if scrape_data:
                rbi_sanction_list.extend(get_rbi_data_list(scrape_data))

    return rbi_sanction_list
    