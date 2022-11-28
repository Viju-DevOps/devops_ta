from eu_parser import eu_parser_utility


def start_eu_parsing(eu_url, folder_name):
    """ Function to parse sanction list from EU url

    Args:
        eu_url: EU sanction list page url
        folder_name: Name of the folder in which file should be downloaded

    Returns: return the sanctioned list from european page

    """
    eu_sanction_list = []
    file_path = eu_parser_utility.download_eu_sanction_list_pdf(eu_url, folder_name)
    if file_path:
        eu_sanction_list = eu_parser_utility.extract_eu_data_from_pdf(file_path)
    return eu_sanction_list


