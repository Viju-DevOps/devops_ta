from us_parser import us_parser_utility


def start_us_parsing(us_url):
    """ Function to parse sanction list from US url

    Args:
        us_url: US sanction list page url

    Returns: return the sanctioned list from US page

    """
    us_sanction_list = []
    scrape_data = us_parser_utility.start_us_web_scraping(us_url)
    if scrape_data:
        us_sanction_list = us_parser_utility.format_us_data(scrape_data)
    return us_sanction_list
