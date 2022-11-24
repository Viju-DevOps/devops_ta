from uk_parser import uk_parser_utility


def start_uk_parsing(uk_url):
    """ Function to parse sanction list from UK url

    Args:
        uk_url: UK sanction list page url

    Returns: return the sanctioned list from uk page

    """
    uk_sanction_list = []
    scrape_data = uk_parser_utility.start_uk_web_scraping(uk_url)
    if scrape_data:
        uk_sanction_list = uk_parser_utility.format_uk_data(scrape_data)
    return uk_sanction_list
